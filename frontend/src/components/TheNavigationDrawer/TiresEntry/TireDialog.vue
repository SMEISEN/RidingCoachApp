<template>
  <div>
    <v-dialog
      v-model="tire_dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card :min-height="window_height">
        <v-toolbar
          dark
          color="primary"
        >
          <v-btn
            icon
            @click.prevent="onTireCancel()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Tires</v-toolbar-title>
          <v-spacer />
        </v-toolbar>
        <TireDialogTabs
          :tire-array="tire_array"
          @refreshTires="$emit('refreshTires')"
        />
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import TireDialogTabs from './TireDialogTabs.vue';

export default {
  name: 'TireDialog',
  components: {
    TireDialogTabs,
  },
  props: {
    tireArray: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    window_height: 0,
  }),
  computed: {
    tire_array() {
      return this.tireArray;
    },
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
    /**
     * Closes the tire dialog.
     */
    onTireCancel() {
      this.tire_dialog = false;
    },
  },
};
</script>
