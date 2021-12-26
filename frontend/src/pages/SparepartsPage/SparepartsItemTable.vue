<template>
  <div>
    <v-form
      ref="validation_form"
      v-model="valid"
    >
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
            <th class="text-center pa-0">
              Stock
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
              class="pl-0 pr-2"
              style="border-bottom: none"
            >
              <v-text-field
                v-model.number="entry.stock"
                class="mb-n2"
                style="font-size: 14px; min-width: 85px"
                height="20px"
                required
                :rules="[v => (v) >= 0]"
                dense
                prepend-icon="mdi-minus"
                append-outer-icon="mdi-plus"
                @click:prepend.prevent="entry.stock = decreaseStock(entry.stock)"
                @click:append-outer.prevent="entry.stock = increaseStock(entry.stock)"
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
    </v-form>
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
  </div>
</template>

<script>
import {
  incrementNumber,
  decrementNumber,
} from '../../components/utils/FromUtils';

export default {
  name: 'SparepartsItemTable',
  props: {
    sparepartChild: {
      type: Array,
      required: true,
    },
    sparepartChildTemplate: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    valid: true,
  }),
  computed: {
    sparepart_child: {
      get() {
        return this.sparepartChild;
      },
      set(value) {
        this.$emit('update:sparepartChild', value);
      },
    },
    sparepart_child_template() {
      return this.sparepartChildTemplate;
    },
  },
  methods: {
    /**
     * Adds a child row to the spare part parent.
     */
    addChildRow() {
      this.sparepart_child.push(this._.cloneDeep(this.sparepart_child_template));
    },
    /**
     * Deletes a child row from the spare part parent.
     */
    deleteChildRow(index) {
      this.sparepart_child.splice(index, 1);
    },
    /**
     * Increases the stock of a spare part item.
     * @param {number} stock
     * @returns {number} updated stock
     */
    increaseStock(stock) {
      return incrementNumber(stock, 1);
    },
    /**
     * Decrease the stock of a spare part item.
     * @param {number} stock
     * @returns {number} updated stock
     */
    decreaseStock(stock) {
      return decrementNumber(stock, 1);
    },
  },
};
</script>

<style scoped>

</style>
