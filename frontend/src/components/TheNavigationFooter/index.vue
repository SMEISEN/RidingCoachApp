<template>
  <v-footer
    fixed
    padless
  >
    <v-row no-gutters>
      <TheNavigationTabs
        @currentPage="setPage"
      />
    </v-row>
  </v-footer>
</template>

<script>
import TheNavigationTabs from '../TheNavigationTabs/index.vue';

export default {
  name: 'TheNavigationFooter',
  components: {
    TheNavigationTabs,
  },
  computed: {
    current_tab: {
      get() {
        return this.currentPage;
      },
      set(value) {
        this.$emit('update:currentPage', value);
      },
    },
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
