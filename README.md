# Hypothesis Testing Statistics Calculator

## Overview
The **Hypothesis Testing Statistics Calculator** is a Flask-based web application designed to assist users in performing various hypothesis tests. This tool simplifies the process of statistical hypothesis testing by providing an intuitive interface and accurate calculations.

## Features
- **Conformity Tests**: Perform one-sample test (Z test, T test and Chi-squared test) on the population's mean, variance or proportion.
- **Comparison Tests**: Perform two-sample comparison test (Z test, T test and Fisher test) on the population's mean, variance or proportion.
- **Independence Tests**: Perform parametric and non parametric independance tests on two random variables.
- **Homogeneity Tests**: Test the equality of some theoritical distribution with a sample's distribution.
- **Multiple Samples Tests**: Perform comparison tests for the mean and variance for multiple samples (ANOVA, Bartlett test and Kruskal-Wallis test)
- **Non-parametric Comparison Tests**: Perform non parametrix tests (Mann-Whitney U test and Wilcoxon signed-rank test) on the samples' means.
- **User-Friendly Interface**: Intuitive input forms and clear result presentations.
- **Real-Time Results**: Get immediate feedback on your hypothesis tests.

## Installation

### Prerequisites
- Python 3.7 or higher

### Dependencies
- Flask
- NumPy
- SciPy


### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kennylalek/Hypothesis-Testing.git
   cd Hypothesis-Testing
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   flask run --port 5001
   ```
   The app will be available at `http://127.0.0.1:5001/`.

## Usage

1. Navigate to the home page of the application.
2. Select the type of hypothesis test you want to perform.
3. Input your data into the provided form.
4. Submit the form to view the test results.


## Contributing
If you would like to contribute to this project, feel free to fork the repository and submit a pull request. Contributions are welcome, whether it's adding new features, fixing bugs, or improving documentation.


## Acknowledgments
- [Flask](https://flask.palletsprojects.com/) for providing a lightweight web framework.
- [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/) for their statistical functions.
- The open-source community for continuous support and resources.
