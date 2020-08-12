<script>
import { Line, mixins } from 'vue-chartjs';

export default {
  name: 'LineChart',
  extends: Line,
  mixins: [
    mixins.reactiveProp,
  ],
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
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
</script>
