# BUET CSE Fest 2024 Treasure Hunt

This repository contains the source code for the BUET CSE Fest 2024 Treasure Hunt website, an interactive platform designed to engage participants in a series of challenges during the event.


## Features

- **User Registration and Authentication**: Participants can create accounts and securely log in to track their progress.
- **Interactive Challenges**: A series of puzzles and tasks that participants must solve to advance.
- **Real-Time Leaderboard**: Displays participant rankings based on challenge completion times.
- **Responsive Design**: Ensures optimal viewing and interaction across various devices.

## Installation

To set up the project locally, follow these steps:

1. **Clone the Repository**:

   ```
   git clone https://github.com/wjalal/bcf24_hunt.git
   ```

2. **Navigate to the Project Directory**:

   ```
   cd bcf24_hunt
   ```

3. **Create a Virtual Environment**:

   Ensure you have Python installed. Then, create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**:

   ```
   pip install -r requirements.txt
   ```

5. **Set Up the Database**:

   ```
   flask db upgrade
   ```

6. **Run the Application**:

   ```
   flask run
   ```

   Access the application at `http://localhost:5000`.

## Usage

1. **Register an Account**:

   Sign up with a username and password to participate in the treasure hunt.

2. **Log In**:

   Access your account using your credentials.

3. **Start the Hunt**:

   Begin solving challenges and advance through the levels.

4. **Track Progress**:

   Monitor your standings on the real-time leaderboard.
