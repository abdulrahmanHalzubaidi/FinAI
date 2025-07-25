import re
from pathlib import Path
from math import floor
import json
import pandas as pd
from textwrap import dedent

from markdown2 import markdown
from jinja2 import Template
from ydata_profiling import ProfileReport
from bs4 import BeautifulSoup

from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.agents import create_pandas_dataframe_agent

from io import StringIO
from werkzeug.datastructures import FileStorage

from .plotting_tools import make_plotting_tools#, scatter_plot, line_plot, bar_plot, stacked_bar_plot, make_inject_df


your_api_key = "INSERT HERE YOUR OPENAI API KEY"



# the path to the prompts dir
PROMPT_DIR = Path(__file__).resolve().parent / 'prompts'

def answer_finai(df, query):
    with open(PROMPT_DIR / 'chatbot_prompt.jinja') as ctemp:
        chat_template = ctemp.read()
    prompt_template = Template(chat_template)
    rendered_prompt = prompt_template.render(query=query)
    
    llm = ChatOpenAI(model="gpt-4o", 
                     api_key=your_api_key)
    agent = create_pandas_dataframe_agent(llm, 
                                          df, 
                                          verbose=True, 
                                          handle_parsing_errors=True, 
                                          allow_dangerous_code=True, 
                                          agent_type=AgentType.OPENAI_FUNCTIONS)
    return agent.run(rendered_prompt)

MIN_QUESTIONS = 2
MAX_QUESTIONS = 3

plot_data = list() # list of tuples

def generate_questions(df, summary, llm, num_questions):
    # convert dict summary to formatted json string
    str_summary = str(summary)
    head = df.head(10).to_string()
    with open(PROMPT_DIR / 'gen_questions_user.jinja') as f:
        template = f.read()
    template = Template(template)
    user_prompt = template.render(summary=str_summary, head=head, num_questions=num_questions)

    with open(PROMPT_DIR / 'gen_questions_system.jinja') as f:
        sys_prompt = f.read()
    
    messages = [
        (
            "system",
            sys_prompt
        ),
        (
            "user",
            user_prompt
        )
    ]
    response = llm.invoke(messages)
    question_dict = json.loads(response.content)
    question_list = list(question_dict.values())
    return question_list

def get_agent_context(df: pd.DataFrame, question: str):
    with open(PROMPT_DIR / 'question_context.jinja') as f:
        template = f.read()
    template = Template(template)
    prompt = template.render(
        head=df.head(5).to_string(),
        describe=df.describe().to_string(),
        dtypes=df.dtypes.to_string(),
        question=question
    )
    return prompt

def get_plot_context(df: pd.DataFrame):
    with open(PROMPT_DIR / 'plotting_context.jinja') as f:
        template = f.read()
    template = Template(template)
    prompt = template.render(
        head=df.head(5).to_string(),
        describe=df.describe().to_string(),
        dtypes=df.dtypes.to_string(),
    )
    return prompt

# Input: json output of ydata profiler
# Output: cleaned up dict with less info and more descriptive names
def get_initial_summary(data, df):
    data = data['variables']
    summary = {}
    
    for key, value in data.items():
        category_summary = {
            'n_distinct': value.get('n_distinct'),
            'n_unique': value.get('n_unique'),
            'count': value.get('count'),
            'type': value.get('type'),
            'pd_summary': df[key].describe()
        }
        
        if 'value_counts_without_nan' in value:
            if (value['n_distinct'] < 10 or value['p_distinct'] < 0.6) and value['n_distinct'] < 15:
                category_summary['value_counts'] = value['value_counts_without_nan']
        
        summary[key] = category_summary
    # print(type(summary))
    # print(summary)
    return summary

def resolve_num_questions(n: int):
    num_questions = floor(n / 50)
    num_questions = max(MIN_QUESTIONS, num_questions)
    num_questions = min(MAX_QUESTIONS, num_questions)
    return num_questions


def create_plot_div(b64_image: str, description: str) -> str:
    return dedent(f'''
    <div class="plot-container">
        <div class="plot">
            <img class="plot-img" src="data:image/png;base64,{b64_image}"/>
            <p class="plot-desc">{description}</p>
        </div>
    </div>
    ''')
    

# Input: csv_path
# Output: markdown formatted full report (str)
def generate_report(csv_path, model='gpt-4o'):
    # 0. setup
    if isinstance(csv_path, FileStorage):
        file_content = csv_path.read().decode('utf-8')
        string_io = StringIO()
        string_io.write(file_content)
        string_io.seek(0)
        csv_path = string_io

    llm = ChatOpenAI(model=model, api_key=your_api_key)
    csv_agent = create_csv_agent(
        llm, 
        csv_path,
        verbose=True,
        handle_parsing_errors=True,
        allow_dangerous_code=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    # 1. bulid df and graphing agent
    if isinstance(csv_path, StringIO):
        csv_path.seek(0)
    df = pd.read_csv(csv_path)
    print(df.head())
    num_questions = resolve_num_questions(len(df))

    tools = make_plotting_tools(df)

    prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a data visualization assistant. Given an analysis question and views of a dataframe, create the most relevant chart using the tools provided."),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ], 
    )
    plotting_agent_base = create_tool_calling_agent(llm, tools, prompt)
    plotting_agent = AgentExecutor(agent=plotting_agent_base, tools=tools, verbose=True)

    # 2. run through combinator to extract structured insights
    profile = ProfileReport(df)
    dict_summary = profile.to_json()
    dict_summary = json.loads(dict_summary)
    ydata_html = profile.to_html() # keep this for later injection for the dynamic viewer


    ### 2A. generate clean summary from dict_summary
    initial_summary = get_initial_summary(dict_summary, df)

    # 3. generate pertinent questions about the data
    questions = generate_questions(df, initial_summary, llm, num_questions)

    # 4. invoke csv agent for each of these questions
    question_report_str = ""
    question_report_str_img = ""
    missed = 0
    for i, question in enumerate(questions, start=1):
        # answer question
        question_prompt = get_agent_context(df, question)
        try:
            result = csv_agent.invoke(question_prompt)
            
        except Exception as e:
            try:
                print(f'Retrying question {i}. Error: {e}')
                result = csv_agent.invoke(question_prompt)
            except Exception as e2:
                print(f'Skipped question {i}. Error: {e2}')
                missed += 1
                continue        
        

        content = list(result.values())[-1]
        
        question_report_str += f'\n### Question {i-missed}: {question}\n{content}'
        #question_report_str_img += f'\n### Question {i-missed}: {question}\n{content}\n{img_div}'
    
    # 5. Ask the *primary* fixed questions from the data
    with open(PROMPT_DIR / 'questions.json') as f:
        questions_dict = json.load(f)
    primary_questions = list(questions_dict.values())
    primary_report_str = ""
    missed = 0
    for i, question in enumerate(primary_questions, start=1):
        # answer question
        question_prompt = get_agent_context(df, question)
        try:
            result = csv_agent.invoke(question_prompt)
        except Exception as e:
            try:
                print(f'Retrying question {i}. Error: {e}')
                result = csv_agent.invoke(question_prompt)
            except Exception as e2:
                print(f'Skipped question {i}. Error: {e2}')
                missed += 1
                continue
        content = list(result.values())[-1]
        primary_report_str += f'\n### Question {i-missed}: {question}\n{content}\n'

    # 6. Join both question-answer reports
    context_qa = f'\n## Primary questions\n{primary_report_str}\n\n## Secondary exploratory questions\n{question_report_str}'

    # 7. Invoke LLM to generate executive summary based on all q-a pairs and other views
    ### Build the summary 
    with open(PROMPT_DIR / 'executive_prompt_system.jinja') as f:
        sys_prompt = f.read()
    with open(PROMPT_DIR / 'executive_prompt_user.jinja') as f:
        user_prompt = f.read()
    
    head = df.head().to_string()

    user_prompt = Template(user_prompt).render(
        head=head,
        summary=str(initial_summary),
        report=context_qa
    )
    
    messages = [
        ('system', sys_prompt),
        ('user', user_prompt)
    ]
    executive_summary = llm.invoke(messages).content

    # generate plots
    
    retries = 3
    for attempt in range(retries):
        try:
            plot_result = plotting_agent.invoke({
                'input': get_plot_context(df)
            })
            if len(plot_data) < 2:
                continue
            break  # successful
        except Exception as e:
            #plot_data.clear()
            print(f"Plotting_agent: attempt {attempt + 1} failed: {e}")
            # if attempt == retries - 1:
            #     raise # raise if all tries fail

    # 8. Merge and convert report
    full_report = f'{executive_summary}\n\n{create_plot_div(*plot_data.pop())}'
    full_report = re.sub(
        r'^(?=## Insights)',  # lookahead for "## Insights"
        f'{create_plot_div(*plot_data.pop())}\n',
        full_report,
        flags=re.MULTILINE    # so that ^ matches start of lines
    )
    full_report = f'\n{full_report}'

    full_report = markdown(full_report, extras=["tables"], safe_mode=False)

    # 9. Add classes to headers
    soup = BeautifulSoup(full_report)

    for h2 in soup.find_all('h2', string=re.compile(r'.*Insight.*', re.IGNORECASE)):
        h2['class'] = ['insights']

    for h2 in soup.find_all('h2', string=re.compile(r'.*overview.*', re.IGNORECASE)):
        h2['class'] = ['overview']
        
    plot_data.clear()
    full_report = soup.prettify()
    return full_report


