function generateDeadlinesCalendar(calendarYear) {
    const calendar = document.getElementById('calendar');
    const monthLabels = document.getElementById('month-labels');
    const deadlinesFrequency = JSON.parse(
        document.getElementById('deadlines-frequency-data').textContent
    );

    let currentYearStart = new Date(calendarYear, 0, 1, 0, 0, 0);
    let currentMonth = 0;

    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    let numberOfColumns = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0
    }

    let nextYearStart = new Date(calendarYear + 1, 0, 1, 0, 0, 0);

    while (currentYearStart < nextYearStart) {
        const column = document.createElement('div');
        column.classList.add('column');

        numberOfColumns[currentMonth]++;

        for (let dayOfTheWeek = 0; dayOfTheWeek < currentYearStart.getDay(); dayOfTheWeek++) {
            const day = document.createElement('div');
            day.classList.add('day');
            day.style.background = 'none';
            column.appendChild(day);
        }

        for (let dayOfTheWeek = currentYearStart.getDay(); dayOfTheWeek < 7; dayOfTheWeek++) {
            if (currentYearStart >= nextYearStart || currentYearStart.getMonth() > currentMonth) {
                break;
            }

            let deadlineDate = currentYearStart.getFullYear() + "-";

            if (currentYearStart.getMonth() + 1 < 10)
                deadlineDate += "0" + (currentYearStart.getMonth() + 1) + "-";
            else
                deadlineDate += (currentYearStart.getMonth() + 1) + "-";

            if (currentYearStart.getDate() < 10)
                deadlineDate += "0" + currentYearStart.getDate();
            else
                deadlineDate += currentYearStart.getDate();

            const day = document.createElement('a');
            day.classList.add('day');
            day.href = document.getElementById('main-page-main-script').dataset.toDoListPageUrl + "?deadline=" + deadlineDate;
            column.appendChild(day);

            const currentDate = currentYearStart.getFullYear() + "-" + currentYearStart.getMonth() + "-" + currentYearStart.getDate();

            if (currentDate in deadlinesFrequency) {
                const currentDeadlineFrequency = deadlinesFrequency[currentDate];
                if (currentDeadlineFrequency === 1)
                    day.classList.add('level-1');
                else if (currentDeadlineFrequency <= 3)
                    day.classList.add('level-2');
                else
                    day.classList.add('level-3');
            }

            currentYearStart.setDate(currentYearStart.getDate() + 1);
        }

        if (currentYearStart.getMonth() > currentMonth) {

            if (currentYearStart.getDay() > 0) {
                for (let dayOfTheWeek = currentYearStart.getDay(); dayOfTheWeek < 7; dayOfTheWeek++) {
                    const day = document.createElement('div');
                    day.classList.add('day');
                    day.style.background = 'none';
                    column.appendChild(day);
                }
            }

            currentMonth++;
        }

        calendar.appendChild(column);

        if (numberOfColumns[currentMonth] === 0) {
            const emptyColumn = document.createElement('div');
            emptyColumn.classList.add('column');
            for (let dayOfTheWeek = 0; dayOfTheWeek < 7; dayOfTheWeek++) {
                const day = document.createElement('div');
                day.classList.add('day');
                day.style.background = 'none';
                emptyColumn.appendChild(day);
            }

            calendar.appendChild(emptyColumn);
        }
    }

    let prevColumns = 0;
    for (const [monthNumber, columns] of Object.entries(numberOfColumns)) {
        const label = document.createElement('div');
        label.classList.add('month-label');

        if (prevColumns !== 0)
            label.style.marginLeft = (prevColumns * 13) + 'px';

        label.textContent = months[monthNumber];
        monthLabels.appendChild(label);

        prevColumns = columns - 1;
    }
}

function deleteDeadlinesCalendar() {
    // deleting the calendar columns
    const calendar = document.getElementById('calendar');
    while (calendar.hasChildNodes()) {
        const firstChildNode = calendar.firstChild;
        calendar.removeChild(firstChildNode);
    }

    // deleting the calendar month labels
    const monthLabels = document.getElementById('month-labels');
    while (monthLabels.hasChildNodes()) {
        const firstChildNode = monthLabels.firstChild;
        monthLabels.removeChild(firstChildNode);
    }
}

(() => {
    let currentDatetime = document.currentScript.dataset.datetime;
    const [date, time] = currentDatetime.split("T")
    const [currentYear, currentMonth, currentDay] = date.split("-").map(Number)
    // const [tmpHourString, tmpMinuteString, secondsExtended] = time.split(":")
    // const [tmpSecondsString, fractionalSeconds_Timezone] = secondsExtended.split(".")

    // const currentHour = Number(tmpHourString)
    // const currentMinute = Number(tmpMinuteString)
    // const currentSeconds = Number(tmpSecondsString)

    const currentYearBtn = document.getElementById('btnCurrentYear');
    currentYearBtn.textContent = currentYear;

    const nextYearBtn = document.getElementById('btnNextYear');
    nextYearBtn.textContent = currentYear + 1;

    generateDeadlinesCalendar(currentYear);

    currentYearBtn.addEventListener('click', () => {
        if ((currentYearBtn.classList.value).includes('active') == false) {

            deleteDeadlinesCalendar();
            generateDeadlinesCalendar(currentYear);

            currentYearBtn.classList = "btn current-year-btn active";
            nextYearBtn.classList = "btn next-year-btn";
        }
    });

    nextYearBtn.addEventListener('click', () => {
        if ((nextYearBtn.classList.value).includes('active') == false) {
            deleteDeadlinesCalendar();
            generateDeadlinesCalendar(currentYear + 1);

            nextYearBtn.classList = "btn next-year-btn active";
            currentYearBtn.classList = "btn current-year-btn";
        }
    });

})();