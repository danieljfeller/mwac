<!-- eslint-disable @typescript-eslint/no-non-null-assertion -->

<template>
    <svg ref="chart"></svg>
</template>

<script lang="ts">
import * as d3 from "d3";
import { PropType, defineComponent, ref } from "vue";

interface SnowData {
    dayOfWinter: number;
    depthCm: number;
    date?: Date;
    year?: number;
    month?: number;
    monthDay?: string;
    winter: string;
}

export default defineComponent({
    name: "LineGraph",
    data(): {
        info: string;
        svg:
            | d3.Selection<SVGSVGElement, undefined, null, undefined>
            | undefined;
        data: SnowData[] | undefined;
        path:
            | d3.Selection<
                  d3.BaseType | SVGPathElement,
                  (number | undefined)[][] & {
                      z: number | undefined;
                  },
                  SVGGElement,
                  undefined
              >
            | undefined;
        line: d3.Line<[number, number]> | undefined;
        dot: d3.Selection<SVGGElement, undefined, null, undefined> | undefined;
        points: (string | number)[][] | undefined;
    } {
        return {
            line: undefined,
            info: "",
            svg: undefined,
            data: undefined,
            path: undefined,
            dot: undefined,
            points: undefined,
        };
    },
    props: {
        height: Object as PropType<number>,
        width: Object as PropType<number>,
    },
    async mounted() {
        const height = this.height ?? 600;
        const width = this.width ?? 928;
        const marginTop = 20;
        const marginRight = 20;
        const marginBottom = 30;
        const marginLeft = 30;

        const parentElement = ref('chart');

        this.data = await this.getData();
        console.log(this.data);

        const x = d3
            .scaleLinear()
            .domain([0, d3.max(this.data, (d) => d.dayOfWinter as any)])

            .range([marginLeft, width - marginRight]);

        const y = d3
            .scaleLinear()
            .domain([0, d3.max(this.data, (d) => d.depthCm as any)])
            .nice()
            .range([height - marginBottom, marginTop]);

        this.svg = d3
            .select(this.$refs.chart as any)
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr(
                "style",
                "max-width: 100%; height: auto; overflow: visible; font: 10px sans-serif;"
            ) as d3.Selection<SVGSVGElement, undefined, null, undefined>;

        // X-axis
        this.svg
            .append("g")
            .attr("transform", `translate(0,${height - marginBottom})`)
            .call(
                d3
                    .axisBottom(x)
                    .ticks(width / 80)
                    .tickSizeOuter(0)
            );

        // Y-axis
        this.svg
            .append("g")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(d3.axisLeft(y))
            .call((g) => g.select(".domain").remove())
            .call((g) =>
                g
                    .append("text")
                    .attr("x", -marginLeft)
                    .attr("y", 10)
                    .attr("fill", "currentColor")
                    .attr("text-anchor", "start")
                    .text("Snow Depth (cm)")
            );

        this.points = this.data.map((d) => [
            x(d.dayOfWinter),
            y(d.depthCm),
            d.winter,
        ]);

        const groups = d3.rollup(
            this.points,
            (v) => Object.assign(v, { z: v[0][2] }),
            (d) => d[2]
        );

        this.line = d3.line();
        this.path = this.svg
            .append("g")
            .attr("fill", "none")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .selectAll("path")
            .data(groups.values())
            .join("path")
            //.style("mix-blend-mode", "multiply")
            .attr("d", this.line as any)
            .attr("stroke-width", (d: any)=>{
                if (d.z == "Average Winter") {
                    
                    return 3;
                } else {
                    
                    return 1.5
                }
            })
            .attr("stroke", (d: any) => {
                console.log(d.z);
                // Assuming "average winter group" is identified by a property like d.key
                if (d.z == "Average Winter") {
                    console.log('yay');
                    return "red"; // Change color to red for average winter group
                } else {
                    return "steelblue"; // Keep color as steelblue for other groups
                }
            }) as any;


    

        this.dot = this.svg.append("g").attr("display", "none");

        this.dot.append("circle").attr("r", 2.5);

        this.dot.append("text").attr("text-anchor", "middle").attr("y", -8);

        // this.path?.filter((d: any) => {
        //     if (d.z == "Average Winter"){
        //         console.log('avg')
        //         return true;
        //     } else {
        //         return false;
        //     }
        // }).each(()=>{
        //     (parentElement.value as any).appendChild(this);
        // })

        this.path
                ?.filter(({ z }) => {
                    if ((z as any) == "Average Winter") console.log('cool');
                    return (z as any) === "Average Winter"
                }
                    )
                .raise();
     
        

        this.svg
            .on("pointerenter", this.pointerEntered)
            .on("pointermove", this.pointerMoved)
            .on("pointerleave", this.pointerLeft)
            .on("touchstart", (event) => event.preventDefault());
    },
    methods: {
        pointerEntered(event: any) {
            this.path
                // .style("mix-blend-mode", null)
                ?.style("stroke", "#ddd");
            this.dot?.attr("display", null);
        },
        pointerMoved(event: any) {
            const [xm, ym] = d3.pointer(event);
            const i = d3.leastIndex(this.points!, ([x, y]) =>
                Math.hypot((x as number) - xm, (y as number) - ym)
            );
            const [x, y, k] = this.points![i!];
          
            this.path
                ?.style("stroke", ({ z }) => (z === k ? null : "#ddd"))
                .filter(({ z }) => z === k)
                .raise();
            this.dot?.attr("transform", `translate(${x},${y})`);
            this.dot?.select("text").text(k as any);
            (this.svg?.property("value", this.data![i!]) as any).dispatch(
                "input",
                {
                    bubbles: true,
                }
            );
        },
        pointerLeft(event: any) {
            this.path
                // ?.style("mix-blend-mode", "multiply")
                ?.style("stroke", null);
            this.dot?.attr("display", "none");
            (this.svg as any).node().value = null;
            (this.svg as any).dispatch("input", { bubbles: true });
        },
        async getData() {
            const historicalDataRaw = await d3.csv(
                "cleaned_hermit_lake_snowdepth.csv"
            );
            const historicalData: SnowData[] = historicalDataRaw.map((row) => ({
                date: new Date(row.date),
                depthCm: +row.depth_cm, // Convert to number if needed
                year: +row.year,
                month: +row.month,
                day: +row.day,
                monthDay: row.month_day,
                winter: row.winter,
                dayOfWinter: +row.day_of_winter,
            }));

            const historicalAvgRaw = await d3.csv("historical_averages.csv");

            const avgData: SnowData[] = historicalAvgRaw.map((row) => ({
                depthCm: +row.depth_cm,
                winter: "Average Winter",
                dayOfWinter: +row.day_of_winter,
            }));
            return [...historicalData, ...avgData];
        },
    },
});
</script>

<style></style>
