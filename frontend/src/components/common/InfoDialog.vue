<template>
  <v-dialog
    v-model="infoDialog"
    persistent
    max-width="400"
  >
    <v-card>
      <v-card-title class="headline">
        Information
      </v-card-title>
      <v-card-text>
        <p class="text--primary">
          {{ infoText }}
        </p>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="accent"
          text
          @click.prevent="onOkay"
        >
          OK
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'InfoDialog',
  props: {
    infoDialog: {
      type: Boolean,
      required: true,
    },
    infoText: {
      type: String,
      required: true,
    },
  },
  updated() {
  },
  created() {
  },
  methods: {
    onOkay() {
      this.$emit('cancelButtonClicked');
      this.$emit('update:infoDialog', false);
    },
  },
};
</script>

<style scoped>

</style>
