name: Auto Update Calendar

# Triggers: every 5 hours + manual dispatch
on:
  schedule:
    - cron:  '0 */5 * * *'    # At-minute 0, every 5th hour, every day
  workflow_dispatch:         # Allows you to “Run workflow” on demand

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      # 1) Check out your repo code
      - name: Checkout repository
        uses: actions/checkout@v3

      # 2) Install Python 3.11
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      # 3) Install dependencies from requirements.txt
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # 4) Generate the ICS calendar file
      - name: Generate live_calendar.ics
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python auto_generate_calendar.py

      # 5) Commit & push the updated ICS back to GitHub
      - name: Commit and push updated calendar
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add live_calendar.ics
          git commit -m "🗓️ Auto-update live_calendar.ics [skip ci]" || echo "No changes to commit"
          git push

      # 6) Success message
      - name: Notify success
        run: |
          echo "✅ live_calendar.ics has been updated and pushed."
          echo "🔗 Raw ICS URL:"
          echo "https://raw.githubusercontent.com/${{ github.repository }}/main/live_calendar.ics"
