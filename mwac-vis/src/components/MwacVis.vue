<template>
    <div class="hello">
        <h1>{{ msg }}</h1>
        <v-container>
            <v-autocomplete
                variant="outlined"
                v-if="winters"
                label="Select Winter"
                :items="winters"
                v-model="selected"
            >
            </v-autocomplete>
        </v-container>
        <div class="main-display">
            <v-container>
                <v-card class="mx-auto" max-width="400">
                    <v-card-text class="pb-2">
                        <v-row align="center" no-gutters>
                            <v-col class="text-h2" cols="12">
                                {{ hoverPoint?.depthCm }} cm
                            </v-col>
                        </v-row>
                        <v-row align="center" no-gutters>
                            <v-col
                                class="text-h4"
                                :color="getPercentOfAvg()! < 100 ? 'red': 'green' ">
                            
                                {{ getPercentOfAvg() }}%
                            </v-col>
                        </v-row>
                    </v-card-text>

                    

                    

                    <v-divider></v-divider>

                    <v-card-actions class="d-flex justify-center">
                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-subtitle>
                                    {{ hoverPoint?.date?.toDateString() }}
                                </v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>
                    </v-card-actions>
                </v-card>
            </v-container>
            <LineGraph
                v-if="snowData"
                @winter-selected="selectWinter"
                @winter-hover="hoverWinter"
                :selected="selected"
                :data="snowData"
            ></LineGraph>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import LineGraph from "./LineGraph.vue";
import { SnowData } from "@/common/interfaces";
import * as d3 from "d3";

export default defineComponent({
    name: "MwacVis",
    props: {
        msg: String,
    },
    components: {
        LineGraph,
    },
    data(): {
        avgWinterMap: Map<number, number> | undefined;
        snowData: SnowData[] | undefined;
        hoverPoint: SnowData | undefined;
        winters: string[] | undefined;
        selected: string | undefined;
    } {
        return {
            avgWinterMap: undefined,
            hoverPoint: undefined,
            winters: undefined,
            selected: undefined,
            snowData: undefined,
        };
    },
    mounted() {
        this.genData();
    },
    methods: {
        hoverWinter(hover: undefined | number) {
            if (hover && this.snowData) {
                this.hoverPoint = this.snowData[hover];
            } else {
                this.hoverPoint = undefined;
            }
        },
        getPercentOfAvg() {
            if (this.hoverPoint && this.avgWinterMap) {
                var avgDepth =
                    this.avgWinterMap.get(this.hoverPoint.dayOfWinter) ?? 1;
                console.log(avgDepth);
                return Math.floor((this.hoverPoint.depthCm / avgDepth) * 100);
            }
        },
        initWinters(winters: string[]) {
            this.winters = winters;
        },
        selectWinter(winter: string) {
            if (winter == this.selected) {
                this.selected = undefined;
            } else {
                this.selected = winter;
            }
        },
        async genData() {
            const historicalDataRaw = await d3.csv(
                "cleaned_hermit_lake_snowdepth.csv"
            );

            const winters: Set<string> = new Set();

            const historicalData: SnowData[] = historicalDataRaw.map((row) => {
                winters.add(row.winter);
                return {
                    date: new Date(row.date),
                    depthCm: +row.depth_cm,
                    year: +row.year,
                    month: +row.month,
                    day: +row.day,
                    monthDay: row.month_day,
                    winter: row.winter,
                    dayOfWinter: +row.day_of_winter,
                };
            });

            this.winters = [...winters];

            const historicalAvgRaw = await d3.csv("historical_averages.csv");

            const avgWinterMap: Map<number, number> = new Map();

            const avgData: SnowData[] = historicalAvgRaw.map((row) => {
                avgWinterMap.set(+row.day_of_winter, +row.depth_cm);
                return {
                    depthCm: +row.depth_cm,
                    winter: "Average Winter",
                    dayOfWinter: +row.day_of_winter,
                };
            });
            this.avgWinterMap = avgWinterMap;

            const snow = [...historicalData, ...avgData];
            this.snowData = snow;

            this.hoverPoint = snow[30];
            console.log(this.snowData);
        },
    },
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.main-display {
    display: flex;
    flex-direction: row;
}

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
