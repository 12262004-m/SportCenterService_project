<template>
  <div>
    <h2>Расписание тренировок</h2>
    <coach-filter :coaches="allCoaches" @filter-by-coach="filterScheduleByCoach" />
    <table>
      <thead>
      <tr>
        <th>День недели</th>
        <th>Зал</th>
        <th>Секция</th>
        <th>Время</th>
        <th>Тренеры</th>
      </tr>
      </thead>
      <tbody>
      <template v-for="day in daysOfWeek" :key="day">
        <tr v-if="!filteredSchedule[day] || filteredSchedule[day].length === 0">
          <td>{{ dayNames[day] }}</td>
          <td colspan="4">Нет тренировок</td>
        </tr>
        <tr v-for="(training, index) in filteredSchedule[day]" :key="training.id">
          <td v-if="index === 0">{{ dayNames[day] }}</td>
          <td v-else></td>
          <td>{{ training.sport_hall }}</td>
          <td>{{ training.sport_section }}</td>
          <td>{{ training.start_time }} - {{ training.end_time }}</td>
          <td>
            <span v-if="training.coach">
              {{ training.coach.lastName }} {{ training.coach.firstName }} {{ training.coach.middleName }}
            </span>
            <span v-else>Нет тренера</span>
          </td>
        </tr>
      </template>
      </tbody>
    </table>
  </div>
</template>

<script>
import CoachFilter from "./ScheduleCoachesFilter.vue";

export default {
  components: {
    CoachFilter,
  },
  data() {
    return {
      schedule: {
        monday: [],
        tuesday: [],
        wednesday: [],
        thursday: [],
        friday: [],
        saturday: [],
        sunday: [],
      },
      filteredSchedule: {},
      allCoaches: [],
      daysOfWeek: [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
      ],
      dayNames: {
        monday: "Понедельник",
        tuesday: "Вторник",
        wednesday: "Среда",
        thursday: "Четверг",
        friday: "Пятница",
        saturday: "Суббота",
        sunday: "Воскресенье",
      },
    };
  },
  methods: {
    async fetchSchedule() {
      const query = `
      query {
        allSchedule {
        id
        weekday
        start
        end
        getHall { name }
        getSection { title }
        getCoach {
          id
          lastName
          firstName
          middleName
          }
         }
        }
      `;
      try {
        const response = await fetch('http://localhost:8000/graphql/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query }),
        });
        const result = await response.json();
        this.allSchedule = result.data.allSchedule;

        const groupedSchedule = {
          monday: [],
          tuesday: [],
          wednesday: [],
          thursday: [],
          friday: [],
          saturday: [],
          sunday: [],
        };

        this.allSchedule.forEach((item) => {
          const dayKey = item.weekday.toLowerCase();
          if (groupedSchedule[dayKey]) {
            groupedSchedule[dayKey].push({
              id: item.id,
              sport_hall: item.getHall?.name || "Нет зала",
              sport_section: item.getSection?.title || "Нет секции",
              start_time: item.start,
              end_time: item.end,
              coach: {
                id: item.getCoach?.id,
                lastName: item.getCoach?.lastName,
                firstName: item.getCoach?.firstName,
                middleName: item.getCoach?.middleName,
              },
            });
          }
        });

        this.schedule = groupedSchedule;
        this.filteredSchedule = JSON.parse(JSON.stringify(groupedSchedule));
      } catch (error) {
        console.error("Ошибка загрузки расписания:", error);
      }
    },

    async fetchAllCoaches() {
      try {
        const response = await fetch("http://localhost:8000/graphql", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            query: `
              query {
                getAllCoaches {
                  id
                  lastName
                  firstName
                  middleName
                }
              }
            `,
          }),
        });
        const result = await response.json();
        this.allCoaches = result.data.getAllCoaches;
      } catch (error) {
        console.error("Ошибка загрузки списка тренеров:", error);
      }
      console.log(this.allCoaches)
    },

    filterScheduleByCoach(coachId) {
      if (!coachId) {
        this.filteredSchedule = JSON.parse(JSON.stringify(this.schedule));
        return;
      }

      const filtered = {};
      Object.keys(this.schedule).forEach((day) => {
        filtered[day] = this.schedule[day].filter(
          (training) => training.coach && training.coach.id === coachId
        );
      });

      this.filteredSchedule = filtered;
    },
  },

  mounted() {
    this.fetchSchedule();
    this.fetchAllCoaches();
  },
};
</script>

<style scoped>
div {
  margin: 3%;
}

h2 {
  text-align: center;
  color: #1F2937;
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

table tr:nth-child(even) td {
  background-color: #f4f4f4;
}

table tr:hover {
  background-color: #ddd;
}

table td,
table th {
  text-align: center;
}

table td ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

table td ul li {
  margin: 5px 0;
  color: #3771f3;
}
</style>
