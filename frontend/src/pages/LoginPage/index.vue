<template v-slot:default>
  <v-app>
    <v-container>
      <v-row
        align="center"
        justify="center"
      >
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="4"
        >
          <LoginForm
            :loading.sync="loading"
            @loginButtonClicked="login"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import { AUTH_REQUEST } from '../../store/actions/authentication';
import LoginForm from './LoginForm.vue';

export default {
  name: 'Login',
  metaInfo: {
    title: 'Login',
  },
  components: {
    LoginForm,
  },
  data: () => ({
    loading: false,
  }),
  methods: {
    login(username, password) {
      this.$store.dispatch(AUTH_REQUEST, { username, password })
        .then(() => {
          this.$router.push('/dashboard');
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'Login successful!',
          });
        })
        .catch((error) => {
          this.loading = false;
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
  },
};
</script>

<style scoped>

</style>
