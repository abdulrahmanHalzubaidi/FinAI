// Formula configurations
const formulas = {
    fv: {
        name: 'Future Value',
        formula: 'FV = PV × (1 + r)^n',
        description: `Purpose
Calculates the future worth of an investment by applying compound interest over time, helping investors understand potential returns.

Formula
FV = PV × (1 + r)^n

Inputs Required
- Present Value (PV): Initial investment amount
- Interest Rate (r): Annual interest rate as a percentage
- Time Period (n): Number of years`,
        inputs: [
            { id: 'pv', label: 'Starting Amount ($)', type: 'number', placeholder: 'Enter starting amount (e.g., 1000)' },
            { id: 'rate', label: 'Yearly Interest Rate (%)', type: 'number', placeholder: 'Enter rate (e.g., 5)' },
            { id: 'time', label: 'Investment Years', type: 'number', placeholder: 'Enter years (e.g., 5)' }
        ],
        calculate: (inputs) => {
            const pv = parseFloat(inputs.pv);
            const rate = parseFloat(inputs.rate) / 100;
            const time = parseFloat(inputs.time);
            return pv * Math.pow(1 + rate, time);
        }
    },
    pv: {
        name: 'Present Value',
        formula: 'PV = FV / (1 + r)^n',
        description: `Purpose
Determines the current worth of a future sum of money, considering the time value of money and discounting future cash flows.

Formula
PV = FV / (1 + r)^n

Inputs Required
- Future Value (FV): Expected future amount
- Discount Rate (r): Annual discount rate as a percentage
- Time Period (n): Number of years until receipt`,
        inputs: [
            { id: 'fv', label: 'Future Value', type: 'number', placeholder: 'Enter future amount (e.g., 1000)' },
            { id: 'rate', label: 'Interest Rate (%)', type: 'number', placeholder: 'Enter rate (e.g., 5)' },
            { id: 'time', label: 'Time Period (Years)', type: 'number', placeholder: 'Enter years (e.g., 5)' }
        ],
        calculate: (inputs) => {
            const fv = parseFloat(inputs.fv);
            const rate = parseFloat(inputs.rate) / 100;
            const time = parseFloat(inputs.time);
            return fv / Math.pow(1 + rate, time);
        }
    },
    roi: {
        name: 'Return on Investment',
        formula: 'ROI = ((Current - Initial) / Initial) × 100',
        description: `Purpose
Measures the profitability of an investment by comparing the gain or loss relative to the initial investment amount.

Formula
ROI = ((Current - Initial) / Initial) × 100

Inputs Required
- Current Value: Present worth of investment
- Initial Investment: Original amount invested`,
        inputs: [
            { id: 'current', label: 'Current Value ($)', type: 'number', placeholder: 'Enter current value (e.g., 150)' },
            { id: 'initial', label: 'Initial Investment ($)', type: 'number', placeholder: 'Enter initial value (e.g., 100)' }
        ],
        calculate: (inputs) => {
            const current = parseFloat(inputs.current);
            const initial = parseFloat(inputs.initial);
            return ((current - initial) / initial) * 100;
        }
    },
    cagr: {
        name: 'Compound Annual Growth Rate',
        formula: 'CAGR = (End Value / Start Value)^(1/years) - 1',
        description: `Purpose
Calculates the average annual growth rate of an investment over a specified time period, smoothing out volatility.

Formula
CAGR = (End Value / Start Value)^(1/years) - 1

Inputs Required
- Ending Value: Final investment worth
- Starting Value: Initial investment amount
- Time Period: Number of years`,
        inputs: [
            { id: 'final', label: 'Ending Value ($)', type: 'number', placeholder: 'Enter final value (e.g., 1500)' },
            { id: 'initial', label: 'Starting Value ($)', type: 'number', placeholder: 'Enter initial value (e.g., 1000)' },
            { id: 'years', label: 'Number of Years', type: 'number', placeholder: 'Enter years (e.g., 5)' }
        ],
        calculate: (inputs) => {
            const final = parseFloat(inputs.final);
            const initial = parseFloat(inputs.initial);
            const years = parseFloat(inputs.years);
            return (Math.pow(final / initial, 1 / years) - 1) * 100;
        }
    },
    compound: {
        name: 'Compound Interest',
        formula: 'A = P(1 + r/n)^(nt)',
        description: `Compound Interest Calculator

What it tells you:
Total savings when interest is earned on your interest.

You need:
• Starting amount
• Yearly interest rate (%)
• Number of years
• How often interest is added:
  Yearly = 1
  Monthly = 12
  Daily = 365

Example: $1,000 at 5%, compounded monthly for 5 years`,
        inputs: [
            { id: 'principal', label: 'Starting Amount ($)', type: 'number', placeholder: 'Enter starting amount (e.g., 1000)' },
            { id: 'rate', label: 'Yearly Interest Rate (%)', type: 'number', placeholder: 'Enter rate (e.g., 5)' },
            { id: 'time', label: 'Investment Years', type: 'number', placeholder: 'Enter years (e.g., 5)' },
            { id: 'frequency', label: 'Times Compounded Per Year', type: 'number', placeholder: 'Enter frequency (e.g., 12 for monthly)' }
        ],
        calculate: (inputs) => {
            const p = parseFloat(inputs.principal);
            const r = parseFloat(inputs.rate) / 100;
            const t = parseFloat(inputs.time);
            const n = parseFloat(inputs.frequency);
            return p * Math.pow(1 + r/n, n*t);
        }
    },
    ratio: {
        name: 'Current Ratio',
        formula: 'Current Ratio = Current Assets / Current Liabilities',
        description: `Purpose
Assesses a company's ability to pay its short-term obligations by comparing current assets to current liabilities.

Formula
Current Ratio = Current Assets / Current Liabilities

Inputs Required
- Current Assets: Cash and assets convertible within one year
- Current Liabilities: Debts due within one year`,
        inputs: [
            { id: 'assets', label: 'Current Assets ($)', type: 'number', placeholder: 'Enter current assets (e.g., 100000)' },
            { id: 'liabilities', label: 'Current Liabilities ($)', type: 'number', placeholder: 'Enter current liabilities (e.g., 50000)' }
        ],
        calculate: (inputs) => {
            const assets = parseFloat(inputs.assets);
            const liabilities = parseFloat(inputs.liabilities);
            return assets / liabilities;
        }
    },
    loan: {
        name: 'Monthly Loan Payment',
        formula: 'PMT = P × (r(1+r)^n) / ((1+r)^n-1)',
        description: `Purpose
Calculates the fixed monthly payment required to repay a loan over a specified period, including both principal and interest.

Formula
PMT = P × (r(1+r)^n) / ((1+r)^n-1)

Inputs Required
- Loan Amount (P): Total amount borrowed
- Interest Rate (r): Annual interest rate as a percentage
- Term (n): Number of monthly payments`,
        inputs: [
            { id: 'principal', label: 'Loan Amount ($)', type: 'number', placeholder: 'Enter loan amount (e.g., 10000)' },
            { id: 'rate', label: 'Yearly Interest Rate (%)', type: 'number', placeholder: 'Enter rate (e.g., 5)' },
            { id: 'months', label: 'Number of Months', type: 'number', placeholder: 'Enter months (e.g., 36)' }
        ],
        calculate: (inputs) => {
            const principal = parseFloat(inputs.principal);
            const annualRate = parseFloat(inputs.rate) / 100;
            const monthlyRate = annualRate / 12;
            const months = parseFloat(inputs.months);
            return principal * (monthlyRate * Math.pow(1 + monthlyRate, months)) / (Math.pow(1 + monthlyRate, months) - 1);
        }
    },
    simpleInterest: {
        name: 'Simple Interest',
        formula: 'I = P × r × t',
        description: `Purpose
Calculates the interest earned on a principal amount over a specific time period, without considering compounding.

Formula
I = P × r × t

Inputs Required
- Principal (P): Initial amount invested
- Interest Rate (r): Annual interest rate as a percentage
- Time (t): Number of years`,
        inputs: [
            { id: 'principal', label: 'Principal Amount ($)', type: 'number', placeholder: 'Enter principal (e.g., 1000)' },
            { id: 'rate', label: 'Annual Interest Rate (%)', type: 'number', placeholder: 'Enter rate (e.g., 5)' },
            { id: 'time', label: 'Time in Years', type: 'number', placeholder: 'Enter years (e.g., 3)' }
        ],
        calculate: (inputs) => {
            const principal = parseFloat(inputs.principal);
            const rate = parseFloat(inputs.rate) / 100;
            const time = parseFloat(inputs.time);
            return principal * rate * time;
        }
    },
    breakEven: {
        name: 'Break-Even Point',
        formula: 'BEP = Fixed Costs / (Price - Variable Cost)',
        description: `Purpose
Determines the number of units that must be sold to cover all costs, helping businesses understand their minimum sales requirements.

Formula
BEP = Fixed Costs / (Price - Variable Cost)

Inputs Required
- Fixed Costs: Ongoing expenses not dependent on production
- Price: Selling price per unit
- Variable Cost: Cost per unit produced`,
        inputs: [
            { id: 'fixedCosts', label: 'Fixed Costs ($)', type: 'number', placeholder: 'Enter fixed costs (e.g., 10000)' },
            { id: 'price', label: 'Price per Unit ($)', type: 'number', placeholder: 'Enter price per unit (e.g., 50)' },
            { id: 'variableCost', label: 'Variable Cost per Unit ($)', type: 'number', placeholder: 'Enter variable cost (e.g., 30)' }
        ],
        calculate: (inputs) => {
            const fixedCosts = parseFloat(inputs.fixedCosts);
            const price = parseFloat(inputs.price);
            const variableCost = parseFloat(inputs.variableCost);
            return fixedCosts / (price - variableCost);
        }
    },
    debtEquity: {
        name: 'Debt to Equity Ratio',
        formula: 'D/E = Total Liabilities / Total Equity',
        description: `Purpose
Measures a company's financial leverage by comparing its total liabilities to shareholders' equity.

Formula
D/E = Total Liabilities / Total Equity

Inputs Required
- Total Liabilities: All outstanding debts and obligations
- Total Equity: Shareholders' equity or net worth`,
        inputs: [
            { id: 'liabilities', label: 'Total Liabilities ($)', type: 'number', placeholder: 'Enter total liabilities (e.g., 100000)' },
            { id: 'equity', label: 'Total Equity ($)', type: 'number', placeholder: 'Enter total equity (e.g., 200000)' }
        ],
        calculate: (inputs) => {
            const liabilities = parseFloat(inputs.liabilities);
            const equity = parseFloat(inputs.equity);
            return liabilities / equity;
        }
    },
    grossMargin: {
        name: 'Gross Profit Margin',
        formula: 'Gross Margin = ((Revenue - COGS) / Revenue) × 100',
        description: `Purpose
Calculates the percentage of revenue that remains after accounting for the cost of goods sold, indicating production efficiency.

Formula
Gross Margin = ((Revenue - COGS) / Revenue) × 100

Inputs Required
- Revenue: Total sales income
- Cost of Goods Sold (COGS): Direct costs of producing goods`,
        inputs: [
            { id: 'revenue', label: 'Revenue ($)', type: 'number', placeholder: 'Enter revenue (e.g., 100000)' },
            { id: 'cogs', label: 'Cost of Goods Sold ($)', type: 'number', placeholder: 'Enter COGS (e.g., 60000)' }
        ],
        calculate: (inputs) => {
            const revenue = parseFloat(inputs.revenue);
            const cogs = parseFloat(inputs.cogs);
            return ((revenue - cogs) / revenue) * 100;
        }
    },
    npv: {
        name: 'Net Present Value',
        formula: 'NPV = -Initial Investment + Σ(Cash Flow / (1 + r)^t)',
        description: `Purpose
Evaluates the profitability of an investment by comparing the present value of cash inflows to the initial investment.

Formula
NPV = -Initial Investment + Σ(Cash Flow / (1 + r)^t)

Inputs Required
- Initial Investment: Upfront cost of the investment
- Cash Flow: Annual cash inflow
- Discount Rate (r): Required rate of return
- Time Period (t): Number of years`,
        inputs: [
            { id: 'initial', label: 'Initial Investment ($)', type: 'number', placeholder: 'Enter initial investment (e.g., 10000)' },
            { id: 'cashflow', label: 'Yearly Cash Flow ($)', type: 'number', placeholder: 'Enter yearly cash flow (e.g., 2000)' },
            { id: 'rate', label: 'Discount Rate (%)', type: 'number', placeholder: 'Enter rate (e.g., 10)' },
            { id: 'years', label: 'Number of Years', type: 'number', placeholder: 'Enter years (e.g., 5)' }
        ],
        calculate: (inputs) => {
            const initial = parseFloat(inputs.initial);
            const cashflow = parseFloat(inputs.cashflow);
            const rate = parseFloat(inputs.rate) / 100;
            const years = parseFloat(inputs.years);
            let npv = -initial;
            for (let t = 1; t <= years; t++) {
                npv += cashflow / Math.pow(1 + rate, t);
            }
            return npv;
        }
    },
    peRatio: {
        name: 'Price to Earnings Ratio',
        formula: 'P/E = Stock Price / Earnings per Share',
        description: `Purpose
Evaluates a company's stock price relative to its earnings, helping investors assess valuation.

Formula
P/E = Stock Price / Earnings per Share

Inputs Required
- Stock Price: Current market price per share
- Earnings per Share: Company's profit per share`,
        inputs: [
            { id: 'price', label: 'Stock Price ($)', type: 'number', placeholder: 'Enter stock price (e.g., 50)' },
            { id: 'eps', label: 'Earnings per Share ($)', type: 'number', placeholder: 'Enter EPS (e.g., 2.5)' }
        ],
        calculate: (inputs) => {
            const price = parseFloat(inputs.price);
            const eps = parseFloat(inputs.eps);
            return price / eps;
        }
    },
    dividendYield: {
        name: 'Dividend Yield',
        formula: 'Dividend Yield = (Annual Dividend / Stock Price) × 100',
        description: `Purpose
Measures the return on investment from dividends relative to the stock price.

Formula
Dividend Yield = (Annual Dividend / Stock Price) × 100

Inputs Required
- Annual Dividend: Total yearly dividend per share
- Stock Price: Current market price per share`,
        inputs: [
            { id: 'dividend', label: 'Annual Dividend per Share ($)', type: 'number', placeholder: 'Enter annual dividend (e.g., 2)' },
            { id: 'price', label: 'Current Stock Price ($)', type: 'number', placeholder: 'Enter stock price (e.g., 50)' }
        ],
        calculate: (inputs) => {
            const dividend = parseFloat(inputs.dividend);
            const price = parseFloat(inputs.price);
            return (dividend / price) * 100;
        }
    },
    assetTurnover: {
        name: 'Asset Turnover Ratio',
        formula: 'Asset Turnover = Net Sales / Average Total Assets',
        description: `Purpose
Measures how efficiently a company uses its assets to generate sales revenue.

Formula
Asset Turnover = Net Sales / Average Total Assets

Inputs Required
- Net Sales: Total revenue from sales
- Average Total Assets: Average value of all assets`,
        inputs: [
            { id: 'sales', label: 'Net Sales ($)', type: 'number', placeholder: 'Enter net sales (e.g., 500000)' },
            { id: 'assets', label: 'Average Total Assets ($)', type: 'number', placeholder: 'Enter avg total assets (e.g., 250000)' }
        ],
        calculate: (inputs) => {
            const sales = parseFloat(inputs.sales);
            const assets = parseFloat(inputs.assets);
            return sales / assets;
        }
    },
    operatingMargin: {
        name: 'Operating Margin',
        formula: 'Operating Margin = (Operating Income / Revenue) × 100',
        description: `Purpose
Calculates the percentage of revenue that remains after operating expenses, indicating operational efficiency.

Formula
Operating Margin = (Operating Income / Revenue) × 100

Inputs Required
- Operating Income: Income after operating expenses
- Revenue: Total sales income`,
        inputs: [
            { id: 'operatingIncome', label: 'Operating Income ($)', type: 'number', placeholder: 'Enter operating income (e.g., 50000)' },
            { id: 'revenue', label: 'Revenue ($)', type: 'number', placeholder: 'Enter revenue (e.g., 200000)' }
        ],
        calculate: (inputs) => {
            const operatingIncome = parseFloat(inputs.operatingIncome);
            const revenue = parseFloat(inputs.revenue);
            return (operatingIncome / revenue) * 100;
        }
    },
    quickRatio: {
        name: 'Quick Ratio',
        formula: 'Quick Ratio = (Current Assets - Inventory) / Current Liabilities',
        description: `Purpose
Measures a company's ability to meet short-term obligations using its most liquid assets.

Formula
Quick Ratio = (Current Assets - Inventory) / Current Liabilities

Inputs Required
- Current Assets: Cash and assets convertible within one year
- Inventory: Value of inventory
- Current Liabilities: Debts due within one year`,
        inputs: [
            { id: 'currentAssets', label: 'Current Assets ($)', type: 'number', placeholder: 'Enter current assets (e.g., 100000)' },
            { id: 'inventory', label: 'Inventory ($)', type: 'number', placeholder: 'Enter inventory (e.g., 30000)' },
            { id: 'currentLiabilities', label: 'Current Liabilities ($)', type: 'number', placeholder: 'Enter current liabilities (e.g., 50000)' }
        ],
        calculate: (inputs) => {
            const currentAssets = parseFloat(inputs.currentAssets);
            const inventory = parseFloat(inputs.inventory);
            const currentLiabilities = parseFloat(inputs.currentLiabilities);
            return (currentAssets - inventory) / currentLiabilities;
        }
    }
};

// Main calculator functionality
class FinancialCalculator {
    constructor() {
        this.currentFormula = '';
        this.setupEventListeners();
        this.updateInputFields();
    }

    setupEventListeners() {
        // Formula selection change
        document.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', (e) => {
                document.getElementById('searchInput').value = e.target.textContent;
                this.currentFormula = e.target.getAttribute('data-value');
                this.updateInputFields();
            });
        });

        // Calculate button click
        document.getElementById('calculate-btn').addEventListener('click', () => {
            this.calculate();
        });
    }

    updateInputFields() {
        const container = document.getElementById('input-fields');
        const formula = formulas[this.currentFormula];

        if (this.currentFormula) {
            document.getElementById('formula-display').style.display = 'block';
            document.getElementById('calculate-btn').style.display = 'block';
        }
        
        // Update formula display
        document.getElementById('formula-text').textContent = formula.description;
        
        // Clear existing fields
        container.innerHTML = '';
        
        // Create new input fields
        formula.inputs.forEach(input => {
            const div = document.createElement('div');
            div.className = 'mb-3';
            div.innerHTML = `
                <label class="form-label">${input.label}</label>
                <input type="text" 
                       class="form-control" 
                       id="${input.id}" 
                       placeholder="${input.placeholder}"
                       oninput="validateNumericInput(event)"
                       onkeydown="return event.key !== 'e' && event.key !== 'E' && event.key !== '+' && event.key !== '-'"
                       required>
            `;
            container.appendChild(div);
        });
    }

    calculate() {
        const formula = formulas[this.currentFormula];
        const inputs = {};
        let hasErrors = false;
        
        // Clear previous errors
        document.querySelectorAll('.error-message').forEach(error => error.remove());
        document.querySelectorAll('.is-invalid').forEach(input => input.classList.remove('is-invalid'));
        
        // Validate all inputs
        formula.inputs.forEach(input => {
            const inputElement = document.getElementById(input.id);
            const value = inputElement.value.trim();
            
            if (!value) {
                showError(inputElement, 'This field is required');
                hasErrors = true;
            } else if (isNaN(value)) {
                showError(inputElement, 'Please enter a valid number');
                hasErrors = true;
            } else {
                inputs[input.id] = value;
            }
        });
        
        if (hasErrors) {
            return;
        }

        try {
            // Calculate result
            const result = formula.calculate(inputs);
            
            // Display result
            const resultDiv = document.getElementById('result');
            const resultValue = resultDiv.querySelector('.result-value');
            
            // Format result based on formula type
            let formattedResult;
            if (this.currentFormula === 'roi' || this.currentFormula === 'cagr') {
                formattedResult = result.toFixed(2) + '%';
            } else if (this.currentFormula === 'ratio') {
                formattedResult = result.toFixed(2);
            } else {
                formattedResult = '$' + result.toFixed(2);
            }
            
            // Update result display
            resultValue.textContent = `${formula.name}: ${formattedResult}`;
            resultDiv.style.display = 'block';
        } catch (error) {
            alert('An error occurred during calculation. Please check your inputs.');
        }
    }
}

// Initialize calculator when page loads
document.addEventListener('DOMContentLoaded', () => {
    new FinancialCalculator();
});

function showDropdown() {
    document.getElementById("dropdownMenu").style.display = "block";
}

function filterDropdown() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let dropdown = document.getElementById("dropdownMenu");
    let items = dropdown.querySelectorAll(".dropdown-item");
    let hasVisibleItem = false;

    items.forEach(item => {
        let text = item.textContent.toLowerCase();
        if (text.includes(input)) {
            item.style.display = "block";
            hasVisibleItem = true;
        } else {
            item.style.display = "none";
        }
    });

    dropdown.style.display = hasVisibleItem ? "block" : "none";
}

document.addEventListener("click", function (event) {
    if (!event.target.closest(".position-relative")) {
        document.getElementById("dropdownMenu").style.display = "none";
    }
});

document.querySelectorAll(".dropdown-item").forEach(item => {
    item.addEventListener("click", function () {
        document.getElementById("searchInput").value = this.textContent;
        document.getElementById("dropdownMenu").style.display = "none";
    });
});

// Add numeric input validation function
function validateNumericInput(event) {
    const input = event.target;
    let value = input.value;
    
    // Store cursor position
    const cursorPosition = input.selectionStart;
    
    // Remove any non-numeric characters except decimal point
    value = value.replace(/[^0-9.]/g, '');
    
    // Ensure only one decimal point
    const decimalCount = (value.match(/\./g) || []).length;
    if (decimalCount > 1) {
        value = value.substring(0, value.lastIndexOf('.'));
    }
    
    // Prevent decimal point at the start
    if (value.startsWith('.')) {
        value = '0' + value;
    }
    
    // Update the input value
    input.value = value;
    
    // Restore cursor position
    input.setSelectionRange(cursorPosition, cursorPosition);
    
    // Remove error message if input is valid
    removeError(input);
}

// Add error message display function
function showError(input, message) {
    const formGroup = input.parentElement;
    const errorDiv = formGroup.querySelector('.error-message') || document.createElement('div');
    errorDiv.className = 'error-message text-danger mt-1';
    errorDiv.textContent = message;
    
    if (!formGroup.querySelector('.error-message')) {
        formGroup.appendChild(errorDiv);
    }
    
    input.classList.add('is-invalid');
}

// Add error removal function
function removeError(input) {
    const formGroup = input.parentElement;
    const errorDiv = formGroup.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
    }
    input.classList.remove('is-invalid');
}