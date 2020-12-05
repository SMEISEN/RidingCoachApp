<template>
  <v-dialog
    v-model="spareparts_dialog"
    persistent
    max-width="500px"
  >
    <v-form
      v-if="spareparts_dialog"
      ref="validation_form"
      v-model="valid"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Add spare part</span>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-text-field
                v-model.number="sparepart_parent.name"
                :rules="[v => !!v]"
                label="Name*"
                required
              />
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-select
                v-model.number="sparepart_parent.module"
                :items="bikeModules"
                :rules="[v => !!v]"
                label="Module*"
                required
              />
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-text-field
                v-model.number="sparepart_parent.min_stock"
                label="Warn at stock"
              />
            </v-col>
          </v-row>
          <v-simple-table dense>
            <thead>
              <tr>
                <th
                  class="text-left pa-0"
                  style="min-width: 20px;width: 200px;max-width: 200px"
                >
                  Description
                </th>
                <th class="text-left pa-0">
                  Condition
                </th>
                <th class="text-left pa-0" />
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(entry, index) in sparepart_child"
                :key="index"
              >
                <td
                  class="pl-0 pr-2"
                  style="border-bottom: none"
                >
                  <v-text-field
                    v-model="entry.description"
                    class="mb-n2"
                    style="font-size: 14px"
                    dense
                    height="20px"
                    single-line
                  />
                </td>
                <td
                  class="pl-0 pr-2"
                  style="border-bottom: none"
                >
                  <v-text-field
                    v-model="entry.condition"
                    class="mb-n2"
                    style="font-size: 14px"
                    dense
                    height="20px"
                    single-line
                  />
                </td>
                <td
                  class="pa-0"
                  style="border-bottom: none"
                >
                  <v-btn
                    icon
                    small
                    @click="deleteChildRow(index)"
                  >
                    <v-icon>
                      mdi-delete
                    </v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
          <v-card-text style="height: 50px; position: relative">
            <v-btn
              class="mr-n4 my-3"
              absolute
              x-small
              fab
              top
              right
              color="primary"
              @click.prevent="addChildRow"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-card-text>
          <v-spacer />
          <p class="text--secondary text-sm-right">
            *indicates required field
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="secondary"
            text
            @click.prevent="onCancel"
          >
            Close
          </v-btn>
          <v-btn
            color="secondary"
            :disabled="!valid"
            text
            @click.prevent="onSave"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import { apiPostSparepart } from '../../components/api/SparepartApi';
import { apiPostSparepartitem } from '../../components/api/SparepartitemApi';
import { initObject } from '../../components/utils/FromUtils';

export default {
  name: 'SparepartsDialogForm',
  props: {
    sparepartsDialog: {
      type: Boolean,
      required: true,
    },
    bikeModules: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    sparepart_parent: {
      name: null,
      module: null,
      min_stock: null,
    },
    sparepart_child: [],
    sparepart_child_template: {
      description: 'original',
      condition: 'new',
    },
    valid: true,
  }),
  computed: {
    spareparts_dialog: {
      get() {
        return this.sparepartsDialog;
      },
      set(value) {
        this.$emit('update:sparepartsDialog', value);
      },
    },
  },
  created() {
    this.sparepart_child.push(this._.cloneDeep(this.sparepart_child_template));
  },
  methods: {
    onSave() {
      apiPostSparepart(this.sparepart_parent)
        .then((res) => {
          const payload = this.sparepart_child.map((o) => ({ ...o, sparepart_id: res.data }));
          for (let i = 0; i < this.sparepart_child.length; i += 1) {
            apiPostSparepartitem(payload[i])
              .then(() => {
                if (i === this.sparepart_child.length - 1) {
                  this.$emit('saveButtonClicked');
                  this.spareparts_dialog = false;
                  this.initForm();
                  this.$store.commit('setInfoSnackbar', {
                    state: true,
                    color: 'success',
                    message: 'Spare part(s) added!',
                  });
                }
              })
              .catch((error) => {
                this.$emit('saveButtonClicked');
                this.spareparts_dialog = false;
                this.$store.commit('setInfoSnackbar', {
                  state: true,
                  color: 'error',
                  message: `${error}!`,
                });
              });
          }
        })
        .catch((error) => {
          this.$emit('saveButtonClicked');
          this.spareparts_dialog = false;
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    onCancel() {
      this.$emit('cancelButtonClicked');
      this.initForm();
      this.spareparts_dialog = false;
    },
    addChildRow() {
      this.sparepart_child.push(this._.cloneDeep(this.sparepart_child_template));
    },
    deleteChildRow(index) {
      this.sparepart_child.splice(index, 1);
    },
    initForm() {
      initObject(this.sparepart_parent, null);
      this.sparepart_child = [this._.cloneDeep(this.sparepart_child_template)];
      if (typeof this.$refs.validation_form !== 'undefined') {
        this.$refs.validation_form.resetValidation();
      }
    },
  },
};
</script>

<style scoped>

</style>
