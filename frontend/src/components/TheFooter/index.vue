<template>
  <v-footer
    app
    absolute
  >
    <v-row no-gutters>
      <v-col
        class="primary text-center white--text"
        cols="12"
      >
        {{ new Date().getFullYear() }} — <strong>Riding Coach</strong>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>

export default {
  name: 'TheFooter',
  methods: {
    setPage(test) {
      this.$emit('currentPage', test);
    },
  },
};
</script>
