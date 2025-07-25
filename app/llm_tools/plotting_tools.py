import base64
from io import BytesIO


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

#from langchain.tools import tool
from langchain_core.tools import tool


def _plot_to_b64(fig, description: str) -> tuple:
    """Convert figure to base64 with data quality notice if needed"""
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8'), description

def _check_missing(df: pd.DataFrame, cols: list) -> str:
    """Return warning message if missing data exists"""
    missing = df[cols].isnull().sum().sum()
    return f" (⚠️ {missing} missing values ignored)" if missing > 0 else ""

def make_plotting_tools(injected_df):
    from .finai_llm import plot_data
    
    sns.set_palette("tab10")
    @tool
    def scatter_plot(title: str, description: str, x_col: str, y_col: str) -> str:
        """Generate scatter plot (auto-drops missing values)."""
        try:
            df = injected_df
            plot_df = df[[x_col, y_col]].dropna()
            fig = sns.scatterplot(data=plot_df, x=x_col, y=y_col).get_figure()
            fig.axes[0].set_title(title)
            plt.xticks(rotation=90)
            warning = _check_missing(df, [x_col, y_col])
            result = _plot_to_b64(fig, description + warning)
            plot_data.append(result)
            return "Plot was generated successfully."
        
        except Exception as e:
            return f"Plot generation failed: {str(e)}"

    @tool
    def line_plot(title: str, description: str, x_col: str, y_col: str) -> str:
        """Generate line plot (auto-drops missing values)."""
        try:
            df = injected_df
            plot_df = df[[x_col, y_col]].dropna().sort_values(x_col)
            fig = sns.lineplot(data=plot_df, x=x_col, y=y_col).get_figure()
            fig.axes[0].set_title(title)
            plt.xticks(rotation=90)

            warning = _check_missing(df, [x_col, y_col])
            result = _plot_to_b64(fig, description + warning)
            plot_data.append(result)
            return "Plot generated successfully"
        except Exception as e:
            return f"Plot generation failed: {str(e)}"

    @tool
    def bar_plot(title: str, description: str, x_col: str, y_col: str) -> str:
        """Generate bar plot (auto-fills missing with 0). y_col must be numeric. Will only show top 5 categories if more exist."""
        try:
            df = injected_df
            plot_df = df[[x_col, y_col]].fillna(0)

            # Get top 5 categories by sum of y_col values
            if plot_df[x_col].nunique() > 5:
                top_categories = plot_df.groupby(x_col)[y_col].sum().nlargest(5).index
                plot_df = plot_df[plot_df[x_col].isin(top_categories)]
            
            fig = sns.barplot(data=plot_df, x=x_col, y=y_col, hue=x_col, errorbar=None).get_figure()
            fig.axes[0].axhline(0, color='black', linewidth=0.8)
            fig.axes[0].set_title(title)
            plt.xticks(rotation=90)

            warning = _check_missing(df, [x_col, y_col])
            if plot_df[x_col].nunique() > 5:
                warning += "\nNote: Showing only top 5 categories."

            result = _plot_to_b64(fig, description + warning.replace("ignored", "filled with 0"))
            plot_data.append(result)
            return "Plot generated successfully"
        except Exception as e:
            return "Plot generation failed."
    
    @tool
    def stacked_bar_plot(title: str, description: str, x_col: str, y_col: str, stack_col: str) -> str:
        """Generate stacked bar plot using Seaborn (auto-fills missing with 0)."""
        max_categories = 5
        try:
            df = injected_df
            plot_df = df[[x_col, y_col, stack_col]].fillna(0)
            
            # Convert stack categories to string if not already
            plot_df[stack_col] = plot_df[stack_col].astype(str)
            
            if pd.api.types.is_numeric_dtype(plot_df[y_col]):
                # Sum duplicates if numeric
                plot_df = plot_df.groupby([x_col, stack_col])[y_col].sum().unstack(fill_value=0)
            else:
                # Count occurrences if non-numeric
                plot_df = plot_df.groupby([x_col, stack_col]).size().unstack(fill_value=0)
            
            # Limit number of categories
            if len(plot_df.columns) > max_categories:
                # Sort categories by total value (sum across all x values)
                top_categories = plot_df.sum().sort_values(ascending=False).head(max_categories - 1).index
                other_categories = [col for col in plot_df.columns if col not in top_categories]
                
                # Combine smaller categories into 'Other'
                plot_df['Other'] = plot_df[other_categories].sum(axis=1)
                plot_df = plot_df[list(top_categories) + ['Other']]
            
            # Prepare data for seaborn
            plot_df = plot_df.reset_index().melt(id_vars=x_col, var_name=stack_col, value_name=y_col)
            
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(
                data=plot_df,
                x=x_col,
                y=y_col,
                hue=stack_col,
                estimator=sum,
                errorbar=None,
                dodge=False
            )
            
            ax.axhline(0, color='black', linewidth=0.8)
            ax.set_title(title)
            plt.xticks(rotation=90)
            plt.legend(title=stack_col, bbox_to_anchor=(1.05, 1), loc='upper left')
            
            warning = _check_missing(df, [x_col, y_col, stack_col])
            result = _plot_to_b64(plt.gcf(), description + warning.replace("ignored", "filled with 0"))
            plot_data.append(result)
            return "Plot generated successfully"
        except Exception as e:
            return f"Plot generation failed: {str(e)}"
        
    @tool
    def histogram_plot(title: str, description: str, col: str) -> str:
        """
        Histogram with adaptive binning. For use with numeric data types.
        Drops null values.
        """
        try:
            n_cats = 5
            df = injected_df
            if pd.api.types.is_numeric_dtype(df[col]):
                # Numerical data - use smart binning
                q75, q25 = np.percentile(df[col].dropna(), [75, 25])
                bin_width = 2 * (q75 - q25) / (len(df[col]) ** (1/3))
                bins = int((df[col].max() - df[col].min()) / bin_width)
                fig = sns.histplot(df[col], bins=min(bins, 30)).get_figure()
                fig.axes[0].set_title(title)
            else:
                # Categorical data - show top N
                counts = df[col].value_counts()
                top = counts.head(n_cats)
                fig = plt.figure()
                plt.bar(top.index.astype(str), top.values)
                if len(counts) > n_cats:
                    plt.bar("Other", counts[n_cats:].sum())
                plt.title(title)
                plt.xticks(rotation=90)

            warning = _check_missing(df, [col])
            if not pd.api.types.is_numeric_dtype(df[col]) and df[col].nunique() > n_cats:
                warning += f"\nNote: Showing only top {n_cats} categories."

            result = _plot_to_b64(fig, description + warning)
            plot_data.append(result)
            return "Plot generated successfully"
        except Exception as e:
            return f"Plot generation failed: {str(e)}"
        
    @tool
    def top_frequency_barplot(
        title: str, 
        description: str, 
        category_col: str
    ) -> str:
        """
        Bar plot of the top 5 (at most) frequent categories. 
        Missing values are auto-dropped.
        """
        try:
            df = injected_df[[category_col]].dropna()
            max_categories = 5
            
            # Get top N categories by frequency
            top_categories = df[category_col].value_counts().nlargest(max_categories)
            plot_df = top_categories.reset_index()
            plot_df.columns = [category_col, "count"]  # Rename for barplot
            
            # Plot
            fig, ax = plt.subplots()
            sns.barplot(
                data=plot_df, 
                x=category_col, 
                y="count",
                hue=category_col,
                errorbar=None,
                ax=ax
            )
            ax.set_title(title)
            plt.xticks(rotation=90) 
            
            # Handle missing values warning
            warning = _check_missing(injected_df, [category_col])
            
            result = _plot_to_b64(
                fig, 
                description + warning
            )
            plot_data.append(result)
            return "Plot generated successfully."
        
        except Exception as e:
            return f"Plot generation failed: {str(e)}"
    
    @tool
    def top_category_boxplot(
        title: str,
        description: str,
        category_col: str,
        numeric_col: str
    ) -> str:
        """
        Boxplot of a numeric column across top 5 (at most) most frequent categories.
        Missing values are auto-dropped.
        """
        try:
            df = injected_df[[category_col, numeric_col]].dropna()
            max_categories = 5

            # Limit to top N categories
            top_cats = df[category_col].value_counts().nlargest(max_categories).index
            plot_df = df[df[category_col].isin(top_cats)]

            # Plot
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(
                data=plot_df,
                x=category_col,
                y=numeric_col,
                ax=ax
            )
            ax.set_title(title)
            ax.set_xlabel(category_col)
            ax.set_ylabel(numeric_col)
            plt.xticks(rotation=90)

            # Handle missing values warning
            warning = _check_missing(injected_df, [category_col, numeric_col])
            
            result = _plot_to_b64(
                fig,
                description + warning
            )
            plot_data.append(result)
            return "Plot generated successfully."
        
        except Exception as e:
            return f"Plot generation failed: {str(e)}"


    
    tools = [
        #line_plot,
        #scatter_plot,
        #stacked_bar_plot,
        top_category_boxplot,
        bar_plot,
        top_frequency_barplot,
        histogram_plot
    ]

    return tools