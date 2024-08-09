# PhonePe Pulse Data Visualization and Exploration

## Introduction

This project involves the development of a Streamlit application designed for analyzing and visualizing transactions and user data from the PhonePe Pulse dataset. The dataset was cloned from the [PhonePe Pulse GitHub repository](https://github.com/PhonePe/pulse). The application provides insights into various aspects of the data, including states, years, quarters, districts, transaction types, and user brands.

The primary goal of this application is to facilitate exploration of data trends and patterns, thereby supporting decision-making processes within the Fintech industry.

## Key Features

- **Interactive Dashboard**: Visualize trends and patterns using interactive plots and charts.
- **Data Exploration**: Explore transactions and user data segmented by states, years, quarters, districts, transaction types, and user brands.
- **Comprehensive EDA**: Perform Exploratory Data Analysis (EDA) to uncover insights and optimize strategies.

## Technologies and Skills

- **Python**: Programming language used for data analysis and application development.
- **Streamlit**: Framework for building interactive web applications.
- **Plotly**: Library for creating interactive plots and charts.
- **Pandas**: Data manipulation and analysis library.
- **MySQL**: Database management system used for data storage.
- **Git**: Version control system for managing code changes.

## Getting Started

To run this project locally, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ManojBalakrishnan22/Phonepe-Pulse-Data-Visualization-and-Exploration.git
    cd your-directory
    ```

2. **Install Dependencies**:
    Make sure you have Python installed. Then, install the necessary Python packages using pip:
    ```bash
    pip install mysql-connector-python gitpython streamlit streamlit-option-menu plotly pandas
    ```

3. **Set Up the Database**:
    Configure MySQL and import the dataset into the database. Update the database connection settings in application code .

4. **Run the Streamlit Application**:
    Start the Streamlit application using the following command:
    ```bash
    streamlit run data_visualization.py
    ```

5. **Access the Dashboard**:
    Open your web browser and navigate to `http://localhost:8501` to interact with the dashboard.

## Dataset

The dataset used in this project is the PhonePe Pulse dataset, which includes various data points related to transactions and users across different states and time periods.

## Screenshots
**Explore Data**
![explore_data](https://github.com/user-attachments/assets/39d1352d-8a9f-4d8c-bb0e-58c54b173ffb)

**Top charts**
![top_charts](https://github.com/user-attachments/assets/73bfe648-4687-40b5-96a6-c3a7d3bc1fc0)


## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## Acknowledgments

- [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse) for providing the dataset.
- [Streamlit](https://streamlit.io) and [Plotly](https://plotly.com) for their powerful tools that enabled the creation of this interactive application.

---

For any questions or feedback, please contact [bmanoj1122000@gmail.com](mailto:bmanoj1122000@gmail.com).
