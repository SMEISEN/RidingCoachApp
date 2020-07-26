<template>
  <v-dialog
    v-model="advice_dialog"
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
  >
    <v-card :min-height="window_height">
      <v-stepper
        v-model="current_step"
        vertical
      >
        <v-stepper-step
          :complete="current_step > 1"
          step="1"
        >
          Select bike end
        </v-stepper-step>
        <v-stepper-content step="1">
          <v-card
            color="blue-grey lighten-5"
            class="mb-3"
            :height="0.5 * window_height"
          >
            <v-slide-group
              v-model="bike_end_slide_group"
              center-active
              show-arrows
              class="py-12"
            >
              <v-slide-item
                v-for="n in 2"
                :key="n"
                v-slot:default="{ active, toggle }"
              >
                <v-card
                  :color="active ? 'primary' : 'blue-grey lighten-4'"
                  :height="0.35 * window_height"
                  width="170"
                  class="mx-4"
                  @click="toggle"
                >
                  <v-row
                    class="fill-height"
                    align="center"
                    justify="center"
                  >
                    <v-scale-transition>
                      <v-icon
                        v-if="active"
                        color="white"
                        size="48"
                        v-text="'mdi-close-circle-outline'"
                      ></v-icon>
                    </v-scale-transition>
                  </v-row>
                </v-card>
              </v-slide-item>
            </v-slide-group>
          </v-card>
          <v-card-actions>
            <v-spacer />
            <v-btn
              text
              @click="advice_dialog = false"
            >
              Cancel
            </v-btn>
            <v-btn
              color="primary"
              @click="current_step = 2"
            >
              Continue
            </v-btn>
          </v-card-actions>
        </v-stepper-content>
        <v-stepper-step
          :complete="current_step > 2"
          step="2"
        >
          Describe symptom
        </v-stepper-step>
        <v-stepper-content step="2">
          <v-card
            color="grey lighten-1"
            class="mb-3"
            :height="0.5 * window_height"
          >
            test
          </v-card>
          <v-card-actions>
            <v-spacer />
            <v-btn
              text
              @click="advice_dialog = false"
            >
              Cancel
            </v-btn>
            <v-btn
              color="primary"
              @click="current_step = 3"
            >
              Continue
            </v-btn>
          </v-card-actions>
        </v-stepper-content>
        <v-stepper-step
          :complete="current_step > 3"
          step="3"
        >
          Choose troubleshooting
        </v-stepper-step>
        <v-stepper-content step="3">
          <v-card
            color="grey lighten-1"
            class="mb-3"
            :height="0.5 * window_height"
          >
            test
          </v-card>
          <v-card-actions>
            <v-spacer />
            <v-btn
              text
              @click="advice_dialog = false"
            >
              Cancel
            </v-btn>
            <v-btn
              color="primary"
              @click="current_step = 1"
            >
              Continue
            </v-btn>
          </v-card-actions>
        </v-stepper-content>
      </v-stepper>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'TrainingDialogAdviceDialog',
  props: {
    adviceDialog: {
      type: Boolean,
      required: true,
    },
  },
  data: () => ({
    current_step: 1,
    window_height: 0,
    bike_end_slide_group: null,
  }),
  computed: {
    advice_dialog: {
      get() {
        return this.adviceDialog;
      },
      set(value) {
        this.$emit('update:adviceDialog', value);
      },
    },
  },
  updated() {
    this.window_height = window.innerHeight;
  },
  created() {
  },
  methods: {

  },
};
</script>

<style scoped>

</style>
