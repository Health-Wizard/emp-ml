<p align="center">
<img src="https://github.com/Health-Wizard/.github/assets/98249720/efb222b5-2dda-466b-b5ce-070e744228f7" alt="IntelliCare Logo" width="260" height="200">

<p align="center">
   <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AI/ML-FC7925?style=for-the-badge" alt="Machine Learning">
</p>

# Mind-Sync

MindSync is an AI-powered platform revolutionizing mental health support in the workplace. Utilizing Large Language Models (LLM) and Natural Language Processing (NLP), it comprehensively analyzes employee data to understand mental well-being.
The platform empowers employees to proactively manage their mental health, offering insights into stress levels, workload impact, and mood variations. Personalized strategies guide individuals through mental health challenges, tailored to their unique circumstances. For organizations, IntelliCare swiftly identifies mental health concerns and encourages timely interventions, fostering a culture that values both productivity and mental well-being.
The platform comprises three components: a visually appealing UI dashboard, a robust backend for smooth communication, and an AI server hosting LLM models for precise health assessments. IntelliCare seamlessly integrates with third-party applications like Slack and Jira to comprehensively analyze employee interactions.
In the corporate landscape, where AI-driven mental health solutions are in high demand, IntelliCare stands out by providing comprehensive health assessments and support to enhance employee well-being and boost productivity.

### Overview

MindSync is a comprehensive mental health assessment and support system designed to analyze and improve the mental well-being of employees within an organization. By leveraging advanced Language Model (LLM) models, the system detects stress levels, emotions, mood, depression, and burnout rates based on employee text messages, survey forms, and engagement games data.
For know more read this [slide](https://docs.google.com/presentation/d/1NkCl5IP7GwxmuZ56yYWFDc75HRhTw2qHEZI3ocAhWfw/edit?usp=sharing)

### Key Features
- Comprehensive Mental Health Analysis:
Utilizes LLM models to perform a thorough analysis of employees' mental health using various forms of employee interactions.

- Data Sources:
Gathers data from text messages, survey forms, and engagement games to provide a holistic understanding of employees' mental well-being.

- Health Attributes Based on Context:
Determines health attributes based on employee roles, salary levels, and departments, allowing for tailored insights and suggestions.

- Graphical Visualization:
Generates graphs and visuals data to present employee health details, facilitating a clear understanding of mental health trends.


### How it Works

MindSense processes the text interactions provided by employees through various channels, such as messaging platforms, survey forms, and engagement games. The language models analyze this text data to determine stress levels, emotions, mood, depression, and burnout rates.

The system considers contextual factors such as role, salary, and department to tailor the analysis and recommendations, ensuring a more personalized approach to mental health assessment.


## SetUp

1. Need to install python in the system
2. create a virtual environment
3. run ```pip install requirements.txt``` in the terminal
4. create a ```.env``` file based on the template
4. run ```uvicorn app.main:app```
5. check port 8000



