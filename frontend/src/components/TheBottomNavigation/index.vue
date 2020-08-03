<template>
  <v-bottom-navigation
    app
    grow
    height="48px"
  >
    <TheNavigationTabs
      @currentPage="setPage"
    />
  </v-bottom-navigation>
</template>

<script>
import TheNavigationTabs from '../TheNavigationTabs/index.vue';

export default {
  name: 'TheBottomNavigation',
  components: {
    TheNavigationTabs,
  },
  created() {
  },
  updated() {
  },
  methods: {
    setPage(test) {
      this.$emit('currentPage', test);
    },
  },
};
</script>

<style scoped>

</style>
