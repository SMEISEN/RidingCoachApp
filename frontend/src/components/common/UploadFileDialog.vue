<template>
  <v-dialog
    v-model="uploadDialog"
    persistent
    max-width="400"
  >
    <v-card>
      <v-card-title class="headline">
        Upload {{ fileCategory }}
      </v-card-title>
      <v-card-text>
        <v-form
          ref="validation_form"
          v-model="valid"
        >
          <v-file-input
            :value="cachedFiles"
            label="File input"
            :rules="rules"
            :accept="fileTypes"
            multiple
            @change="selectFile"
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          id="cancelButton"
          color="accent"
          text
          @click.prevent="onCancel"
        >
          Cancel
        </v-btn>
        <v-btn
          id="uploadButton"
          color="success"
          text
          :disabled="!valid || cachedFiles.length === 0"
          @click.prevent="onUpload"
        >
          Upload
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'UploadFileDialog',
  props: {
    uploadDialog: {
      type: Boolean,
      required: true,
    },
    fileCategory: {
      type: String,
      required: true,
    },
    fileTypes: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    cachedFiles: [],
    valid: true,
  }),
  computed: {
    rules() {
      return [
        (files) => !files || !files.some(
          (file) => !this.fileTypes.includes(file.type),
        ) || 'File type does not match!',
      ];
    },
  },
  methods: {
    /**
     * Updates the cached files.
     * @param files files to be cached
     */
    selectFile(files) {
      this.cachedFiles = files;
      console.log(files);
    },
    /**
     * Emits a message to the parent component that the upload was cancelled and closes the
     * upload dialog.
     */
    onCancel() {
      this.$emit('cancelButtonClicked');
      this.$emit('update:uploadDialog', false);
      this.cachedFiles = [];
      this.$refs.validation_form.resetValidation();
    },
    /**
     * Emits a message to the parent component that the upload was confirmed.
     */
    onUpload() {
      this.$emit('uploadButtonClicked', this.cachedFiles);
      this.$emit('update:uploadDialog', false);
      this.cachedFiles = [];
      this.$refs.validation_form.resetValidation();
    },
  },
};
</script>
