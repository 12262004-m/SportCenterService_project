<template>
  <div class="today_trainings_table">
    <h2>Расписание на {{ dayNamesRu[current_day] }}, {{ current_date }}</h2>
    <div v-if="todaySchedule.length > 0">
      <table>
        <thead>
        <tr>
          <th v-for="(training, hall) in groupedSchedule" :key="hall">
            {{ hall }}
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="rowIndex in maxRows" :key="rowIndex">
          <td v-for="(trainings, gym) in groupedSchedule" :key="gym + '-' + rowIndex">
            <div v-if="trainings[rowIndex - 1]">
              <strong>
                {{ trainings[rowIndex - 1].start || '—' }} - {{ trainings[rowIndex - 1].end || '—' }}
              </strong>
              <br />
              <p>
                {{ trainings[rowIndex - 1].getSection.title || 'Нет секции' }}
              </p>
              <strong class="coach_name">
                {{ trainings[rowIndex - 1].getCoach.lastName + " " + trainings[rowIndex - 1].getCoach.firstName + " " + trainings[rowIndex - 1].getCoach.middleName|| 'Нет тренера' }}
              </strong>
            </div>
            <div v-else>
              —
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <table>
        <thead>
        <tr>
          <th v-for="(trainings, gym) in groupedSchedule" :key="gym">
            {{ gym }}
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="rowIndex in maxRows" :key="rowIndex">
          <td> Нет тренировок</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script>

export default {
  data() {
    return {
      allSchedule: [],
      todaySchedule: [],
      current_day: "",
      current_date: "",
      dayNamesRu: {
        "SUNDAY": 'воскресенье',
        "MONDAY": 'понедельник',
        "TUESDAY": 'вторник',
        "WEDNESDAY": 'среда',
        "THURSDAY": 'четверг',
        "FRIDAY": 'пятница',
        "SATURDAY": 'суббота',
      },
    };
  },
  computed: {
    groupedSchedule() {
      const grouped = {};
      this.todaySchedule.forEach((training) => {
        const gymName = training.getHall.name;
        if (!grouped[gymName]) {
          grouped[gymName] = [];
        }
        grouped[gymName].push(training);
      });
      return grouped;
    },
    maxRows() {
      return Math.max(...Object.values(this.groupedSchedule).map((trainings) => trainings.length), 0);
    },
  },
  mounted() {
    this.fetchSchedule();
  },
  methods: {
    async fetchSchedule() {
      const query = `
        query {
        allSchedule{
          id
          weekday
          start
          end
          getHall {
            name
          }
          getSection {
            title
          }
          getCoach {
            lastName
            firstName
            middleName
          }
        }
      }
      `;
      try {
        const response = await fetch('http://localhost:8000/graphql', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query }),
        });
        const result = await response.json();
        this.allSchedule = result.data.allSchedule;

        const dayNames = {
          0: "SUNDAY",
          1: "MONDAY",
          2: "TUESDAY",
          3: "WEDNESDAY",
          4: "THURSDAY",
          5: "FRIDAY",
          6: "SATURDAY"
        };
        const todayIndex = new Date().getDay();
        console.log('allSchedule:', this.allSchedule);
        console.log('todaySchedule:', this.todaySchedule);
        this.current_day = dayNames[todayIndex];
        this.current_date = new Date().toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'long',
          year: 'numeric',
        });
        this.todaySchedule = this.allSchedule.filter(
          (item) => item.weekday === this.current_day
        );

      } catch (error) {
        console.error('Ошибка при загрузке расписания:', error);
      }
    },
  },
};

</script>

<style scoped>
h2 {
  text-align: left;
  color: #1F2937;
}
.today_trainings_table {
  margin: 3%;
}

.coach_name {
  color: #3771f3;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}

table th {
  background-color: #1F2937;
  color: white;
  font-weight: bold;
}

table td {
  background-color: #f8f8f8;
}

table td, table th {
  text-align: center;
}

table td ul {
  list-style-type: none;
  padding: 0;
}

table td ul li {
  margin: 5px 0;
  color: #3771f3;
}
</style>
