from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
from khayyam import JalaliDate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_birthday', methods=['POST'])
def calculate_birthday():
    try:
        data = request.get_json(force=True)
        calendar_type = data['calendarType']
        year = int(data['year'])
        month = int(data['month'])
        day = int(data['day'])

        today = datetime.today()

        if calendar_type == 'gregorian':
            birth_date = datetime(year, month, day)
            birth_date_jalali = JalaliDate(birth_date)
            birth_date_converted = birth_date_jalali.strftime('%Y-%m-%d')
        elif calendar_type == 'jalali':
            birth_date_jalali = JalaliDate(year, month, day)
            birth_date = birth_date_jalali.todate()
            birth_date_converted = birth_date.strftime('%Y-%m-%d')
        else:
            return jsonify({'error': 'نوع تقویم نامعتبر است.'}), 400

        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        age_months = (today.month - birth_date.month - (today.day < birth_date.day)) % 12
        age_days = (today - birth_date).days % 365 % 30

        next_birthday = datetime(today.year if (today.month, today.day) < (birth_date.month, birth_date.day) else today.year + 1, birth_date.month, birth_date.day)
        days_until_birthday = (next_birthday - today).days
        birth_day_of_week = birth_date.strftime('%A')

        result = {
            'daysUntilBirthday': days_until_birthday,
            'age': f'{age_years} سال و {age_months} ماه و {age_days} روز',
            'birthDayOfWeek': birth_day_of_week,
            'birthDateConverted': birth_date_converted,
            'currentYear': today.year,
            'currentMonth': today.month,
            'currentDay': today.day
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
