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
              v-model="category_slide_group"
              center-active
              show-arrows
              class="py-12"
            >
              <v-slide-item
                v-for="category in coach_categories_array"
                :key="'category/' + category.toLowerCase()"
                v-slot:default="{ active, toggle }"
              >
                <v-card
                  color="blue-grey lighten-4"
                  :height="0.35 * window_height"
                  :width="0.45 * window_width"
                  class="mx-4"
                  @click="toggle"
                >
                  <v-img
                    class="secondary--text align-end"
                    contain
                    :height="0.35 * window_height"
                    :width="0.45 * window_width"
                    :src="`${$publicPath}/assets/coach-category-${category.toLowerCase()}.svg`"
                  >
                    <v-card-title>{{ category }} troubleshooting</v-card-title>
                  </v-img>
                  <v-overlay
                    absolute
                    :value="active"
                  >
                    <v-btn
                      v-if="active"
                      icon
                      x-large
                      @click="active = false"
                    >
                      <v-icon x-large>
                        mdi-close-circle-outline
                      </v-icon>
                    </v-btn>
                  </v-overlay>
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
            color="blue-grey lighten-5"
            class="mb-3"
            :height="0.5 * window_height"
          >
            <v-slide-group
              v-model="symptom_slide_group"
              center-active
              show-arrows
              class="py-12"
            >
              <v-slide-item
                v-for="(symptom, index) in symptom_by_category"
                :key="'symptom/' + index"
                v-slot:default="{ active, toggle }"
              >
                <v-card
                  color="blue-grey lighten-4"
                  :height="0.35 * window_height"
                  :width="0.45 * window_width"
                  class="mx-4"
                  @click="toggle"
                >
                  <v-img
                    class="secondary--text align-end"
                    contain
                    :height="0.35 * window_height"
                    :width="0.45 * window_width"
                    :src="`${$publicPath}/assets/coach-` +
                      `category-${symptom.category.toLowerCase()}-` +
                      `symptom-${symptom.symptom.id.substring(1)}.png`"
                  >
                    <v-card-title>
                      {{ symptom.symptom.id + ': ' + symptom.symptom.name }}
                    </v-card-title>
                  </v-img>
                  <v-overlay
                    absolute
                    :value="active"
                  >
                    <v-btn
                      v-if="active"
                      icon
                      x-large
                      @click="active = false"
                    >
                      <v-icon x-large>
                        mdi-close-circle-outline
                      </v-icon>
                    </v-btn>
                  </v-overlay>
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
            color="blue-grey lighten-5"
            class="overflow-y-auto mb-3"
            :height="0.5 * window_height"
          >
            <v-card-text>
              <v-radio-group
                v-model="troubleshooting_problem_radio"
                :mandatory="false"
              >
                <v-radio
                  v-for="(advice, problem_index) in advices_by_symptom"
                  :key="'advice/' + problem_index"
                  :label="problem_index + ':\t' + advice.problem"
                  :value="problem_index"
                >
                  <v-radio-group
                    v-if="advice.solution.length > 0"
                    v-model="troubleshooting_solution_radio"
                    :mandatory="false"
                  >
                    <v-radio
                      v-for="(solution, sulution_index) in advice.solution"
                      :key="'advice/solution' + sulution_index"
                      :label="solution"
                      :value="index"
                    />
                  </v-radio-group>
                </v-radio>
              </v-radio-group>
            </v-card-text>
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
import { apiGetAllCoaches } from '../../api/CoachApi';

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
    window_width: 0,
    category_slide_group: null,
    symptom_slide_group: null,
    troubleshooting_problem_radio: null,
    troubleshooting_solution_radio: null,
    coach_object: {},
    coach_categories_array: [],
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
    symptom_by_category() {
      if (this.category_slide_group !== null && this.category_slide_group !== undefined) {
        const category = this.coach_categories_array[this.category_slide_group];
        return this.coach_object.filter((i) => i.category === category);
      }
      return [];
    },
    advices_by_symptom() {
      if (this.category_slide_group !== null && this.category_slide_group !== undefined) {
        if (this.symptom_slide_group !== null && this.symptom_slide_group !== undefined) {
          return this.symptom_by_category[this.symptom_slide_group].advice;
        }
      }
      return [];
    },
  },
  updated() {
    this.window_height = window.innerHeight;
    this.window_width = window.innerWidth;
  },
  created() {
    this.getCoach();
  },
  methods: {
    getCoach() {
      apiGetAllCoaches().then((res) => {
        this.coach_object = res.data;
        this.getCoachCategories();
      });
    },
    getCoachCategories() {
      this.coach_categories_array = this._.uniq(
        Object.assign(this.coach_categories_array,
          Object.values(
            this._.mapValues(
              this.coach_object, 'category',
            ),
          )),
      );
    },
  },
};
</script>

<style scoped>
  .v-card__text, .v-card__title {
    word-break: normal; /* maybe !important  */
  }
</style>
