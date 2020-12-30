<script>
import { Line } from 'vue-chartjs';

export default {
  name: 'LineChart',
  extends: Line,
  props: {
    options: {
      type: Object,
      required: true,
    },
    chartData: {
      type: Object,
      required: true,
    },
  },
  watch: {
    chartData: {
      deep: true,
      handler() {
        // eslint-disable-next-line
        this.$data._chart.update();
      },
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
</script>
