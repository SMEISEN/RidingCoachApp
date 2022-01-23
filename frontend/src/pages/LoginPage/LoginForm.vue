<template>
  <v-form
    ref="validation_form"
    v-model="valid"
    class="login"
  >
    <v-card class="card-container">
      <v-toolbar
        color="primary"
        dark
      >
        <v-toolbar-title>Sign in</v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <v-row dense>
          <v-col cols="11">
            <v-text-field
              v-model="username"
              label="Username"
              prepend-icon="mdi-account-circle"
              :rules="[v => !!v]"
              required
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="11">
            <v-text-field
              v-model="password"
              label="Password"
              :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
              :type="show ? 'text' : 'password'"
              prepend-icon="mdi-lock"
              :rules="[v => !!v]"
              required
              @click:append="show = !show"
              @keydown.enter="onLoginButton()"
            />
          </v-col>
        </v-row>
        <br>
        <h4
          v-if="checkVersion"
          class="text--secondary text-right"
        >
          Demo app
        </h4>
        <p
          v-if="checkVersion"
          class="text--secondary text-right"
        >
          Username: foo
          <br>
          Password: bar
        </p>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="secondary"
          :loading="loading"
          :disabled="!valid || loading"
          text
          @click="onLoginButton()"
        >
          Login
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
export default {
  name: 'LoginForm',
  props: {
    loading: {
      type: Boolean,
      required: true,
    },
  },
  data: () => ({
    valid: true,
    show: false,
    username: '',
    password: '',
  }),
  computed: {
    checkVersion() {
      return process.env.VUE_APP_VERSION === 'demo';
    },
  },
  methods: {
    /**
     * Emits the username and password to the parent page and sets loading animation to true.
     */
    onLoginButton() {
      this.$emit('update:loading', true);
      this.$emit('loginButtonClicked', this.username, this.password);
    },
  },
};
</script>
