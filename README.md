

**Schedule Generator**
===========================

**Overview**

`scheduler` is a python-based schedule generator that creates your daily schedule randomly and exports it as a PDF file.

It creates the schedule according to a JSON file you provide. In the JSON file, you should define your projects and the probability you assign to each project of being selected.



**Getting Started**

### Prerequisites

* Python 3.x installed on your system
* A JSON schedule file in the `schedules` directory (an example file is provided)

### Installation

1. Clone the repository: `git clone https://github.com/pmoradi/scheduler.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
4. Install the required python packages: `pip install requirements.txt`

### Running the Application

1. Place your JSON schedule file in the `schedules` directory (Consider the `schedule.json.example` format).
2. Run the application: `python main.py`
3. The generated schedule will be saved as a PDF file in the `export` directory

**Configuration**

The JSON schedule file should have the following structure:
```json
[
    {"title": "PROJECT #1", "probability": 30, "time": 120, "priority": 1},
    {"title": "PROJECT #2", "probability": 20, "time": 120, "priority": 2},
    ...
]
```
The `probability` field represents the likelihood of a schedule being chosen on each day (higher values indicate a higher likelihood). The `priority` field represents the priority of the schedule, which is used to sort the schedules in the final output. The `time` field represents the allocated time to each schedule.

**Customization**

You can customize the produced schedule by modifying the following parameters in `main.py`:

- `daily_work_time`: defines the amount of time you want to allocate for your schedules daily.
- `extra_time`: allows for flexibility in the schedule, enabling the selection of schedules with longer times when there is remaining time in the day. The extra time will be applied with a 50% probability in each day.
- `days`: you can specify the list of days for which you want the scheduler to produce a schedule.

**Output**

The generated schedule will be saved as a PDF file in the `export` directory, named `weekly_schedule.pdf`.

**Example**

In this example the code produces a schedule for `Monday` to `Friday` with 8 hours daily work and with a one-hour flexibility as extra time. `scheduler` reads schedule file from `./schedules/schedule.json` and stored the produced schedule in `./export/weekly_schedule.pdf` directory.

```python
import pdf_producer, scheduler

daily_work_time = 8 * 60 # Minutes of daily work
extra_time = 1 * 60
schedules = scheduler.get_weekly_schedule('./schedules/schedule.json', daily_work_time, extra_time=extra_time, days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

pdf_producer.create_pdf(schedules, './export/weekly_schedule.pdf')
```
