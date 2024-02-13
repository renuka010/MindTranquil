const isLeapYear = (year) => {
  return (
    (year % 4 === 0 && year % 100 !== 0 && year % 400 !== 0) ||
    (year % 100 === 0 && year % 400 === 0)
  );
};
const getFebDays = (year) => {
  return isLeapYear(year) ? 29 : 28;
};
let calendar = document.querySelector('.calendar');
const month_names = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];
let month_picker = document.querySelector('#month-picker');
const dayTextFormate = document.querySelector('.day-text-formate');
const timeFormate = document.querySelector('.time-formate');
const dateFormate = document.querySelector('.date-formate');

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.startsWith(name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const generateSessions = (sessions) => {
  let bground2 = document.querySelector('.bground2');
  bground2.innerHTML = '';
  if(sessions.length === 0) {
    let session = document.createElement('div');
    session.className ='stattext opacity-50 p-2';
    session.innerHTML =' No sessions available for this month.';
    bground2.appendChild(session);
  }
  for (let i = 0; i < sessions.length; i++) {
    let session = document.createElement('div');
    session.className = 'h-16 w-52 p-2 m-2 rounded-md bg-white text-black flex flex-shrink-0 items-center';
    
     // Get the day of the end_time
     let endTime = new Date(sessions[i].end_time);
     let day = endTime.getDate();
 
     // Format the duration as 'XhrYmin'
     let [hours, minutes] = sessions[i].duration.split(':');
     let duration = `${Number(hours)}hr ${Number(minutes)}m`;
     let session_type = (sessions[i].session_type.split(' '))[0];
 
     session.innerHTML = `<div class="" style="width:3rem;"><h1 class="text-4xl font-light font-sans text-darkblue">`+day+`</h1></div>
     <div class="" style="width:8rem;"><h1 class="text-xl font-light font-sans text-darkblue">`+session_type+`</h1></div>
     <div class="" style="width:2rem;"><h1 class="text-xs font-light font-sans text-darkblue">`+duration+`</h1></div>`;

     bground2.appendChild(session);
  }
}

const generateCalendar = async (month, year) => {
  try {
    let days_list = [];
    const response = await fetch(`/webapp/get_active_days_api/?month=${month + 1}&year=${year}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      }
    });
    const data = await response.json();
    days_list = data.active_days;
    sessions = data.sessions;

    generateSessions(sessions);

  let calendar_days = document.querySelector('.calendar-days');
  calendar_days.innerHTML = '';
  let calendar_header_year = document.querySelector('#year');
  let days_of_month = [
      31,
      getFebDays(year),
      31,
      30,
      31,
      30,
      31,
      31,
      30,
      31,
      30,
      31,
    ];

  let currentDate = new Date();

  month_picker.innerHTML = month_names[month];

  calendar_header_year.innerHTML = year;

  let first_day = new Date(year, month);

  for (let i = 0; i <= days_of_month[month] + first_day.getDay() - 1; i++) {

    let day = document.createElement('div');

    if (i >= first_day.getDay()) {
      let current_date = i - first_day.getDay() + 1;
      day.innerHTML = current_date;

      if (days_list!==null && days_list.includes(current_date) ) {
        day.classList.add('active-date');
      }
    }
    calendar_days.appendChild(day);
  }
}catch (error) {
  console.error('Error:', error);
}
};

month_names.forEach((e, index) => {
  let month = document.createElement('div');
  month.innerHTML = `<div>${e}</div>`;

  month.onclick = () => {
    currentMonth.value = index;
    generateCalendar(currentMonth.value, currentYear.value);
    dayTextFormate.classList.remove('hideTime');
    dayTextFormate.classList.add('showtime');
    timeFormate.classList.remove('hideTime');
    timeFormate.classList.add('showtime');
    dateFormate.classList.remove('hideTime');
    dateFormate.classList.add('showtime');
  };
});


document.querySelector('#pre-month').onclick = () => {
  --currentMonth.value;
  if (currentMonth.value < 0) {
    currentMonth.value = 11;
    --currentYear.value;
  }
  generateCalendar(currentMonth.value, currentYear.value);
};

document.querySelector('#next-month').onclick = () => {
  ++currentMonth.value;
  if (currentMonth.value > 11) {
    currentMonth.value = 0;
    ++currentYear.value;
  }
  generateCalendar(currentMonth.value, currentYear.value);
};

let currentDate = new Date();
let currentMonth = { value: currentDate.getMonth() };
let currentYear = { value: currentDate.getFullYear() };
generateCalendar(currentMonth.value, currentYear.value);

const todayShowTime = document.querySelector('.time-formate');
const todayShowDate = document.querySelector('.date-formate');

const currshowDate = new Date();
const showCurrentDateOption = {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  weekday: 'long',
};
const currentDateFormate = new Intl.DateTimeFormat(
  'en-US',
  showCurrentDateOption
).format(currshowDate);
setInterval(() => {
  const timer = new Date();
  const option = {
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
  };
  const formateTimer = new Intl.DateTimeFormat('en-us', option).format(timer);
  let time = `${`${timer.getHours()}`.padStart(
      2,
      '0'
    )}:${`${timer.getMinutes()}`.padStart(
      2,
      '0'
    )}: ${`${timer.getSeconds()}`.padStart(2, '0')}`;
}, 1000);

