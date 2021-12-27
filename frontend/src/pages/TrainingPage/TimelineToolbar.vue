<template>
  <v-toolbar
    top
    short
    flat
  >
    <v-btn-toggle
      v-model="timeline_buttons"
      mandatory
      dense
      style="width:100%"
      active-class="v-btn--active-toolbar"
    >
      <v-menu
        ref="menu"
        v-model="date_menu"
        :close-on-content-click="false"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="white"
            class="primary--text"
            style="min-width:20%"
            x-small
            v-bind="attrs"
            v-on="on"
          >
            {{ displayed_date }}
          </v-btn>
        </template>
        <v-date-picker
          v-model="picked_date"
          type="month"
          scrollable
          no-title
          @input="date_menu = false"
        />
      </v-menu>
      <v-btn
        color="white"
        class="primary--text"
        style="min-width:20%"
        x-small
      >
        {{ new Date().getFullYear() }}
      </v-btn>
      <v-btn
        color="white"
        class="primary--text"
        style="min-width:20%"
        x-small
      >
        {{ new Date(new Date().setMonth(new Date().getMonth() - 1))
          .toLocaleString('en-US', { month: 'short' }) }}
      </v-btn>
      <v-btn
        color="white"
        class="primary--text"
        style="min-width:20%"
        x-small
      >
        {{ new Date().toLocaleString('en-US', { month: 'short' }) }}
      </v-btn>
      <v-btn
        class="primary--text"
        style="min-width:20%"
        x-small
      >
        now
      </v-btn>
    </v-btn-toggle>
  </v-toolbar>
</template>

<script>
export default {
  name: 'TimelineToolbar',
  props: {
    timelineButtons: {
      type: Number,
      required: true,
    },
    pickedDate: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    date_menu: false,
  }),
  computed: {
    timeline_buttons: {
      get() {
        return this.timelineButtons;
      },
      set(value) {
        this.$emit('update:timelineButtons', value);
      },
    },
    picked_date: {
      get() {
        return this.pickedDate;
      },
      set(value) {
        this.$emit('update:pickedDate', value);
      },
    },
    displayed_date() {
      if (this.timelineButtons !== 0) {
        return 'pick';
      } if (this.picked_date === null) {
        return new Date().toLocaleString('en-US',
          {
            year: '2-digit',
            month: 'short',
          });
      }
      const pickedDate = new Date(this.picked_date);
      return `${
        pickedDate.toLocaleString('en-US', { month: 'short' })} ${
        pickedDate.toLocaleString('en-US', { year: '2-digit' })}`;
    },
  },
};
</script>
