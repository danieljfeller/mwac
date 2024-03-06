<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <v-container>
    <v-autocomplete
    v-if="winters"
    label="Select Winter"
    :items="winters"
    v-model="selected"
    >
    </v-autocomplete>
    </v-container>
    <LineGraph @winter-selected="selectWinter" @winters="initWinters" :selected="selected" data-file-name="historical_averages.csv"></LineGraph>

  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import LineGraph from './LineGraph.vue'

export default defineComponent({
  name: "MwacVis",
  props: {
    msg: String,
  },
  components: {
    LineGraph,
  },
  data(): {
    winters: string[] | undefined,
    selected: string | undefined,
  } {
    return {
      winters: undefined,
      selected: undefined,

    }
  },
  methods: {
    initWinters(winters: string[]){
      this.winters = winters;

    },
    selectWinter(winter: string){
      if (winter == this.selected){
        this.selected = undefined;
      } else {
        this.selected = winter;
      }
    }
  }


});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
