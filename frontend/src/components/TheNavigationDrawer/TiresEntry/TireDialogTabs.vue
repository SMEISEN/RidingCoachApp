<template>
    <div>
        <v-tabs
            fixed-tabs
            background-color="secondary"
            dark
        >
            <v-tab>
                Slick
            </v-tab>
            <v-tab>
                Rain
            </v-tab>
        </v-tabs>
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
    </div>
</template>

<script>

export default {
  name: 'TireDialogTabs',
  components: {
  },
  data: () => ({
    tire_panel: [0,1],
  }),
  computed: {
    tire_dialog: {
        get() {
        return this.$store.getters.getTireDialogState;
        },
        set(value) {
        this.$store.commit('setTireDialogState', value);
        },
    },
  },
  updated() {
    this.window_height = window.innerHeight;
  },
  methods: {
      onTireCancel() {
      this.tire_dialog = false;
      this.$refs.validation_tire_form.resetValidation();
    },
  },
};
</script>

<style scoped>

</style>
