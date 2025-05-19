<template>
  <div>
    <h2>Тренеры спортивной школы олимпийского резерва №1</h2>
    <CoachesAddNew />
    <div class="coach-info" v-for="coach in coaches" :key="coach.id">
      <img v-if="coach.gender === 'FEMALE'" src="../../assets/images/coaches-images/female.png" />
      <img v-else src="../../assets/images/coaches-images/male.png" />
      <div class="coach-details">
        <div class="coach-full-information">
          <h3>{{ coach.lastName }} {{ coach.firstName }} {{ coach.middleName }}</h3>
          <p>Дата рождения: {{ coach.dateOfBirth }}</p>
          <p>Квалификация: {{ coach.qualification.toLowerCase() }}</p>
          <p>Опыт работы: {{ coach.experience }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CoachesAddNew from "@/components/coaches/CoachesAddNew.vue";

export default {
  components: {
    CoachesAddNew,
  },
  data() {
    return {
      coaches: [],
    };
  },
  methods: {
    async fetchCoaches() {
      const query = `
        query {
          getAllCoaches {
            id
            lastName
            firstName
            middleName
            gender
            dateOfBirth
            qualification
            experience
          }
        }
      `;
      try {
        const response = await fetch('http://localhost:8000/graphql/', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({query}),
        });
        const result = await response.json();
        this.coaches = result.data.getAllCoaches;
      } catch (error) {
        alert("Ошибка загрузки тренеров:" + error);
      }
    }
  },
  mounted() {
    this.fetchCoaches();
  },
};
</script>

<style scoped>
div {
  margin: 3%;
}

hr {
  border: none;
  border-left: 2px solid #1F2937;
  margin: 0 20px;
}

h2 {
  text-align: center;
  color: #1F2937;
}

.coach-info {
  margin-left: auto;
  margin-right: auto;
  display: flex;
  border: 2px solid #1F2937;
  border-radius: 20px;
}

.coach-details {
  display: flex;
  flex-direction: row;
  flex: 1;
}

.coach-full-information {
  flex: 1;
}

img {
  width: 15%;
  height: 15%;
  border-radius: 50%;
  margin: 2%;
  object-fit: cover;
}

.coach-details h1 {
  margin-bottom: 1%;
}

.coach-details p {
  color: #3771f3;
  margin: 0.5% 0;
}

.coach-sections ul {
  list-style-type: none;
  padding: 0;
}
</style>
