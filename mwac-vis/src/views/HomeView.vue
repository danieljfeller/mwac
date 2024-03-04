<template>
  <div class="home">
    <MwacVis msg="MWAC vis App" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import MwacVis from "@/components/MwacVis.vue"; // @ is an alias to /src

export default defineComponent({
  name: "HomeView",
  components: {
    MwacVis,
  },
});
</script>
