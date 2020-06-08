<template v-slot:default>
  <v-app>
    <v-container>
      <v-row align="center" justify="center">
        <v-col cols="12" xs="12" sm="6" md="4">
          <v-form
            class="login"
            v-model="valid"
            ref="validation_form"
          >
            <v-card class="card-container">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Sign in</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-row dense>
                  <v-col cols="11">
                    <v-text-field label="Username"
                                  prepend-icon="mdi-account-circle"
                                  :rules="[v => !!v]"
                                  required
                                  v-model="username">
                    </v-text-field>
                  </v-col>
                </v-row>
                <v-row dense>
                  <v-col cols="11">
                    <v-text-field label="Password"
                                  prepend-icon="mdi-lock"
                                  :rules="[v => !!v]"
                                  required
                                  v-model="password">
                    </v-text-field>
                  </v-col>
                </v-row>
                <br/>
                <h4 v-if="checkVersion"
                    class="text--secondary text-right">
                  Demo app
                </h4>
                <p v-if="checkVersion"
                   class="text--secondary text-right">
                  Username: foo
                  <br/>
                  Password: bar
                </p>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="secondary" :disabled="!valid"
                         text @click="login">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import { AUTH_REQUEST } from '../store/actions/authentication';

export default {
  name: 'Login',
  metaInfo: {
    title: 'Login',
  },
  data() {
    return {
      username: '',
      password: '',
      valid: true,
    };
  },
  computed: {
    checkVersion() {
      return process.env.VUE_APP_VERSION === 'demo';
    },
  },
  methods: {
    login() {
      const { username, password } = this;
      this.$store.dispatch(AUTH_REQUEST, { username, password })
        .then(() => {
          this.$router.push('/dashboard');
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>

</style>
