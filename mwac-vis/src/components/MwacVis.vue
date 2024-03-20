<template>
     <v-app>
        <v-app-bar color="#03A9F4" dark>
            <!-- Title -->
            <v-toolbar-title>{{ msg }}</v-toolbar-title>

            <!-- Spacer -->
            <!-- <v-spacer></v-spacer> -->

            <!-- Navigation items -->
            <!-- <v-btn text>Home</v-btn>
            <v-btn text>About</v-btn>
            <v-btn text>Contact</v-btn> -->
        </v-app-bar>
    
    <div class="home">
        
        <!-- <div class="title">
            <h1>{{ msg }}</h1>
        </div> -->
        

        <div class="spacer"></div>
        <div class="main-display">
            <div class="side-bar">
                <v-row justify="center">
                    <v-col aling="center" justify="center" cols="10">
                        <v-autocomplete
                            variant="solo"
                            v-if="winters"
                            label="Select Winter"
                            :items="winters"
                            v-model="selected"
                        >
                        </v-autocomplete>
                        <v-card
                            variant="elevated"
                            v-if="hoverPoint"
                            :class="['mx-auto', 'display-card']"
                            max-width="400"
                            mb="4"
                        >
                            <v-card-text class="pb-2">
                                <v-row align="center" no-gutters>
                                    <v-col class="text-h3" cols="12">
                                        {{ Math.floor(hoverPoint?.depthCm) }}
                                        cm
                                    </v-col>
                                </v-row>
                                <v-row align="center" no-gutters>
                                    <v-col
                                        :class="['text-h5', getPercentOfAvg()! < 100 ? 'red-text': 'green-text']"
                                    >
                                        {{ getPercentOfAvg() }}%
                                    </v-col>
                                </v-row>
                            </v-card-text>
                            <v-divider></v-divider>

                            <v-card-actions class="d-flex justify-center">
                                <v-list-item>
                                    <v-list-item-content>
                                        <v-list-item-subtitle>
                                            {{ getHoverPointDate() }}
                                        </v-list-item-subtitle>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-card-actions>
                        </v-card>

                        <v-card
                            v-if="selected"
                            variant="elevated"
                            :class="['mx-auto', 'display-card']"
                            max-width="400 "
                            mb="4"
                        >
                            <v-card-text class="pb-2">
                                <v-row align="center" no-gutters>
                                    <v-col class="text-h3" cols="12">
                                        {{ selected }}
                                    </v-col>
                                </v-row>
                                <v-row align="center" no-gutters>
                                    <v-col
                                        :class="['text-h5', getWinterPecentOfAvg()! < 100 ? 'red-text': 'green-text']"
                                        :color="getWinterPecentOfAvg()! < 100 ? 'red': 'green' "
                                    >
                                        {{ getWinterPecentOfAvg() }}% of Avg
                                    </v-col>
                                </v-row>
                            </v-card-text>
                            <v-divider></v-divider>

                            <v-card-actions class="d-flex justify-center">
                                <!-- <v-btn
                                color="red"
                                variant="elevated"
                                >Click</v-btn> -->
                                <v-list-item>
                                    <v-list-item-content>
                                        <v-list-item-subtitle>
                                            Max depth
                                            {{ getMaxDepth() }}cm
                                        </v-list-item-subtitle>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
            </div>
            <div class="vis-tool" ref="visTool">
                <v-card variant="elevated">
                    <v-card-title>Hermit Lake Snow Depth</v-card-title>
                    <v-card-text>
                        <LineGraph
                            v-if="snowData"
                            @winter-selected="selectWinter"
                            @winter-hover="hoverWinter"
                            :selected="selected"
                            :data="snowData"
                        ></LineGraph>
                    </v-card-text>
                </v-card>
            </div>
        </div>
   
    </div>
    </v-app>
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
        maxVisWid: number;
        maxVisLen: number;
    } {
        return {
            maxVisWid: 0,
            maxVisLen: 0,
            avgWinterMap: undefined,
            hoverPoint: undefined,
            winters: undefined,
            selected: undefined,
            snowData: undefined,
        };
    },
    mounted() {
        this.updateDimensions();
        this.genData();
    },
    methods: {
        updateDimensions() {
            // For updating dimensions of svg
            const visTool = this.$refs.visTool;
            if (visTool) {
                const rect = (visTool as any).getBoundingClientRect();
                this.maxVisWid = rect.width;
                this.maxVisLen = rect.height;
            }
        },
        getHoverPointDate() {
            if (this.hoverPoint?.winter === "Average Winter") {
                return this.getMonthDayFromDOW(this.hoverPoint.dayOfWinter);
            } else {
                return this.hoverPoint?.date?.toDateString();
            }
        },
        getMaxDepth() {
            var max = 0;
            this.snowData
                ?.filter((d) => d.winter === this.selected)
                .forEach((depth) => {
                    max = Math.max(depth.depthCm, max);
                });
            return Math.floor(max);
        },
        hoverWinter(hover: undefined | number) {
            if (hover && this.snowData) {
                this.hoverPoint = this.snowData[hover];
            } else {
                this.hoverPoint = undefined;
            }
        },
        getMonthDayFromDOW(dayOfWinter: number) {
            const referenceDate = new Date(2001, 10, 1); // Month is 0-based in JavaScript

            // Add the number of days to the reference date
            const targetDate = new Date();
            targetDate.setDate(referenceDate.getDate() + dayOfWinter - 1);

            const monthNames = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ];
            const month = monthNames[targetDate.getMonth()];
            return `${month}, ${targetDate.getDate()} `;
        },
        getWinterPecentOfAvg(): number {
            // Get information about selected winter.
            const currentSelectedWinter: SnowData[] =
                this.snowData?.filter((dtp) => dtp.winter == this.selected) ??
                [];
            const daySet: Set<number> = new Set(
                currentSelectedWinter.map((w) => w.dayOfWinter)
            );
            const matchingAvgDays = this.snowData?.filter((d) => {
                return (
                    d.winter === "Average Winter" && daySet.has(d.dayOfWinter)
                );
            });
            const avgSum =
                matchingAvgDays?.reduce((acc, val) => acc + val.depthCm, 0) ??
                NaN;
            const selectedSum =
                currentSelectedWinter?.reduce(
                    (acc, val) => acc + val.depthCm,
                    0
                ) ?? NaN;
            if (isNaN(avgSum) || isNaN(selectedSum)) {
                return NaN;
            }
            return Math.floor((selectedSum / avgSum) * 100);
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
@import "../styles/colors";

.green-text {
    color: $success-color;
}

.spacer {
    margin-top: 3dvh;
}

.red-text {
    color: $error-color;
}

.display-card {
    margin: 10px;
}

.home {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    width: 100vw;
    margin-top: 8vh ;
}
.title {
    background-color: $primary-color;
    color: $text-color;
    display: flex;
    justify-content: center;
}

.main-display {
    display: flex;
    flex-direction: row;
    justify-content: center;
    flex: 1;
}

.side-bar {
    display: flex;
    flex: 15%;
    flex-direction: column;
    flex-wrap: nowrap;
}

.vis-tool {
    display: flex;
    flex: 85%;
    box-sizing: border-box;
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
