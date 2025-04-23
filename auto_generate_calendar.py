name: Auto Update Calendar

on:
  schedule:
    - cron: '0 */5 * * *'  # Every 5 hours
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repo
      uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt || true

    - name: Generate calendar
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        python auto_generate_calendar.py

    - name: Commit and Push .ics
      run: |
        git config user.name "YousefBot"
        git config user.email "actions@github.com"
        git add live_calendar.ics
        git commit -m "🗓️ Auto-update calendar file [skip ci]" || echo "No changes"
        git push --force

    - name: Show Success Message
      run: |
        echo "✅ Calendar successfully updated."
        echo "📅 View it here:"
        echo "🔗 https://raw.githubusercontent.com/dublomasi/live-calender-feed/main/live_calendar.ics"
