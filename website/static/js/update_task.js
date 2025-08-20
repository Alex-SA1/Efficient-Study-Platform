(() => {
    const deadlineInput = document.getElementById('deadline');
    const picker = document.getElementById('picker');

    const monthYear = document.getElementById('month-year');
    const daysDiv = document.getElementById('days');
    const prevBtn = document.getElementById('prev-month');
    const nextBtn = document.getElementById('next-month');

    const hoursSelect = document.getElementById('hours');
    const minutesSelect = document.getElementById('minutes');

    const closeBtn = document.getElementById('btn-close-picker');

    let currentDatetime = document.currentScript.dataset.datetime;

    const [date, time] = currentDatetime.split("T")
    const [tmpYear, tmpMonth, tmpDay] = date.split("-").map(Number)
    const [tmpHourString, tmpMinuteString, secondsExtended] = time.split(":")
    const [tmpSecondsString, fractionalSeconds_Timezone] = secondsExtended.split(".")

    const tmpHour = Number(tmpHourString)
    const tmpMinute = Number(tmpMinuteString)
    const tmpSeconds = Number(tmpSecondsString)

    let currentDate = new Date(tmpYear, tmpMonth - 1, tmpDay, tmpHour, tmpMinute, tmpSeconds);
    let selectedDate = null;
    let selectedHour = 0;
    let selectedMinute = 0;

    function togglePicker(show) {
        if (show == true)
            picker.style.display = 'block'
        else
            picker.style.display = 'none'

        deadlineInput.setAttribute('aria-expanded', show);
    }

    function updateCalendar() {
        daysDiv.innerHTML = '';
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        const months = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'];

        monthYear.textContent = months[month] + " " + year;

        // day of the week for the first day of the month
        const firstDayCurrentMonth = new Date(year, month, 1).getDay();
        const daysNumberCurrentMonth = new Date(year, month + 1, 0).getDate();
        const daysNumberPrevMonth = new Date(year, month, 0).getDate();

        // divs for previous month days
        for (let i = firstDayCurrentMonth - 1; i >= 0; i--) {
            const dayDiv = document.createElement('div');

            dayDiv.classList.add('text-center', 'text-secondary', 'inactive', 'py-1', 'rounded');
            dayDiv.textContent = daysNumberPrevMonth - i;

            daysDiv.appendChild(dayDiv);
        }

        // divs for current month days
        for (let day = 1; day <= daysNumberCurrentMonth; day++) {
            const dayDiv = document.createElement('div');
            dayDiv.classList.add('text-center', 'py-1', 'rounded');
            dayDiv.textContent = day;

            if (tmpDay == day && tmpMonth - 1 == currentDate.getMonth() && tmpYear == currentDate.getFullYear())
                dayDiv.classList.add('text-info')

            if (selectedDate && selectedDate.getFullYear() === year && selectedDate.getMonth() === month && selectedDate.getDate() === day) {
                if (dayDiv.classList.contains('text-info'))
                    dayDiv.classList.remove('text-info')

                dayDiv.classList.add('selected', 'text-success');
            }


            dayDiv.style.cursor = 'pointer';
            dayDiv.addEventListener('click', () => {
                selectedDate = new Date(year, month, day);
                updateCalendar();
                updateSelectedDatetime();
                //togglePicker(false);
            });

            daysDiv.appendChild(dayDiv);
        }

        // divs for next month days (to fill the grid)
        const totalGridCells = daysDiv.children.length;
        const daysNumberToFill = 7 * 6 - totalGridCells;
        for (let day = 1; day <= daysNumberToFill; day++) {
            const dayDiv = document.createElement('div');

            dayDiv.classList.add('text-center', 'text-secondary', 'inactive', 'py-1', 'rounded');
            dayDiv.textContent = day;

            daysDiv.appendChild(dayDiv);
        }
    }

    function fillTimePicker() {
        for (let h = 0; h < 24; h++) {
            const option = document.createElement('option');

            option.value = h;
            option.textContent = h.toString().padStart(2, '0');

            hoursSelect.appendChild(option);
        }

        for (let m = 0; m < 60; m += 5) {
            const option = document.createElement('option');

            option.value = m;
            option.textContent = m.toString().padStart(2, '0');

            minutesSelect.appendChild(option);
        }
    }

    function updateSelectedDatetime() {
        if (!selectedDate) {
            deadlineInput.value = "";
            return;
        }

        selectedHour = parseInt(hoursSelect.value);
        selectedMinute = parseInt(minutesSelect.value);

        const year = selectedDate.getFullYear();
        const month = selectedDate.getMonth() + 1;
        const day = selectedDate.getDate();

        const formattedDate = year + "-" + month.toString().padStart(2, '0') + "-" + day.toString().padStart(2, '0');
        const formattedTime = selectedHour.toString().padStart(2, '0') + ":" + selectedMinute.toString().padStart(2, '0');

        deadlineInput.value = formattedDate + " " + formattedTime;
    }

    prevBtn.addEventListener('click', () => {
        currentDate.setDate(1);
        currentDate.setMonth(currentDate.getMonth() - 1);
        updateCalendar();
    });

    nextBtn.addEventListener('click', () => {
        currentDate.setDate(1);
        currentDate.setMonth(currentDate.getMonth() + 1);
        updateCalendar();
    });

    hoursSelect.addEventListener('change', () => {
        updateSelectedDatetime();
    });

    minutesSelect.addEventListener('change', () => {
        updateSelectedDatetime();
    });


    deadlineInput.addEventListener('click', () => togglePicker(true));

    closeBtn.addEventListener('click', () => {
        togglePicker(false);
    });

    fillTimePicker();
    updateCalendar();

    // loading task selected deadline in input field and also in calendar/time picker
    let selected_deadline = document.currentScript.dataset.taskDeadline;
    if (selected_deadline !== "None") {
        const months_abbreviation = {
            'Jan': 0,
            'Feb': 1,
            'Mar': 2,
            'Apr': 3,
            'May': 4,
            'Jun': 5,
            'Jul': 6,
            'Aug': 7,
            'Sept': 8,
            'Oct': 9,
            'Nov': 10,
            'Dec': 11
        };

        const hours_pm = {
            "1": "13",
            "2": "14",
            "3": "15",
            "4": "16",
            "5": "17",
            "6": "18",
            "7": "19",
            "8": "20",
            "9": "21",
            "10": "22",
            "11": "23",
            "12": "12"
        }

        let [selected_deadline_month_day, selected_deadline_year, selected_deadline_time] = selected_deadline.split(", ")
        let [selected_deadline_month, selected_deadline_day] = selected_deadline_month_day.split(". ")

        if (selected_deadline_time !== "midnight") {
            var [selected_deadline_hm, selected_deadline_ot] = selected_deadline_time.split(" ")
            var [selected_deadline_hour, selected_deadline_minutes] = selected_deadline_hm.split(":")

            if (selected_deadline_minutes === undefined)
                selected_deadline_minutes = "00"

            if (selected_deadline_ot === "p.m.")
                selected_deadline_hour = hours_pm[selected_deadline_hour]
            else if (selected_deadline_ot === "a.m." && selected_deadline_hour === "12")
                selected_deadline_hour = "00"
        }
        else {
            var selected_deadline_hour = "00"
            var selected_deadline_minutes = "00"
        }

        selected_deadline_year = parseInt(selected_deadline_year)

        selected_deadline_month = months_abbreviation[selected_deadline_month]
        selected_deadline_month = parseInt(selected_deadline_month)

        selected_deadline_day = parseInt(selected_deadline_day)

        hoursSelect.value = parseInt(selected_deadline_hour)
        minutesSelect.value = parseInt(selected_deadline_minutes)

        selectedDate = new Date(selected_deadline_year, selected_deadline_month, selected_deadline_day);
        updateCalendar();
        updateSelectedDatetime();
    }

})();

function toggleCategories() {
    const btnToggle = document.getElementById('btnToggle');
    const hiddenCategories = document.querySelectorAll('.category.hidden');

    if (btnToggle.value == 'show-more') {
        btnToggle.value = 'show-less';
        btnToggle.textContent = 'Show Less';

        hiddenCategories.forEach(category => category.style.display = 'inline-block');
    }
    else {
        btnToggle.value = 'show-more';
        btnToggle.textContent = 'Show More';

        hiddenCategories.forEach(category => category.style.display = 'none');
    }
}
