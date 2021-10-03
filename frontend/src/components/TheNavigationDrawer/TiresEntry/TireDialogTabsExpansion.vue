<template>
  <v-expansion-panels
    v-model="tire_panel"
    multiple
  >
    <v-expansion-panel>
      <v-expansion-panel-header>Front</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-container>
          </v-container>
        </v-expansion-panel-content>
    </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header>Rear</v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-container>
            </v-container>
          </v-expansion-panel-content>
      </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>

export default {
  name: 'TireDialogTabsExpansion',
  components: {
  },
  props: {
    tireArray: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    tire_panel: [0,1],
  }),
};
</script>

<style scoped>

</style>