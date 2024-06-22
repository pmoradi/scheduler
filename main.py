import pdf_producer, scheduler

daily_work_time = 8 * 60 # Minutes of daily work
extra_time = 1 * 60
schedules = scheduler.get_weekly_schedule('./schedules/schedule.json', daily_work_time, extra_time=extra_time, days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

pdf_producer.create_pdf(schedules, './export/weekly_schedule.pdf')
