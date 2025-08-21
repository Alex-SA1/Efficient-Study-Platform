(() => {
    const calendar = document.getElementById('calendar');
    const calendarTitle = document.getElementById('calendar-title');
    const monthLabels = document.getElementById('month-labels');
    const deadlinesFrequency = JSON.parse(
        document.getElementById('deadlines-frequency-data').textContent
    );

    let currentDatetime = document.currentScript.dataset.datetime;
    const [date, time] = currentDatetime.split("T")
    const [tmpYear, tmpMonth, tmpDay] = date.split("-").map(Number)
    // const [tmpHourString, tmpMinuteString, secondsExtended] = time.split(":")
    // const [tmpSecondsString, fractionalSeconds_Timezone] = secondsExtended.split(".")

    // const tmpHour = Number(tmpHourString)
    // const tmpMinute = Number(tmpMinuteString)
    // const tmpSeconds = Number(tmpSecondsString)

    const yearTitle = document.createElement('h6');
    yearTitle.textContent = tmpYear;
    calendarTitle.appendChild(yearTitle);

    let currentYearStart = new Date(tmpYear, 0, 1, 0, 0, 0);
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

    let nextYearStart = new Date(tmpYear + 1, 0, 1, 0, 0, 0);

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
            day.href = document.currentScript.dataset.toDoListPageUrl + "?deadline=" + deadlineDate;
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

})();