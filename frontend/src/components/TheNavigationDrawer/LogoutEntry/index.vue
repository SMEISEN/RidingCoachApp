<template>
  <v-list-item @click="onLogout">
    <v-list-item-icon>
      <v-icon>mdi-logout</v-icon>
    </v-list-item-icon>
    <v-list-item-title>
      Logout
    </v-list-item-title>
  </v-list-item>
</template>

<script>
import { AUTH_LOGOUT } from '../../../store/actions/authentication';

export default {
  name: 'TheNavigationDrawerLogout',
  methods: {
    /**
     * Logs the user out and proceed to the login page.
     */
    onLogout() {
      this.$store.dispatch(AUTH_LOGOUT);
      this.$router.push('/login');
    },
  },
};
</script>
