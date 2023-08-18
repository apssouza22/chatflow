import Chart from "react-apexcharts";
import {getRenderInfo} from "../command/Common";

type RenderChartProps = {
    data: any
}

export function RenderChart(props: RenderChartProps) {
    const renderInfo = getRenderInfo()
    let x_name = Object.keys(props.data[0])[0]
    let y_name = ""
    if (renderInfo.fields.length > 1) {
        x_name = renderInfo.fields[0]
        y_name = renderInfo.fields[1]
    }
    if (renderInfo.fields.length == 1) {
        y_name = renderInfo.fields[0]
    }
    const axises = props.data.reduce((acc: any, item: any) => {
        acc.x.push(item[x_name])
        acc.y.push(item[y_name])
        return acc
    }, {x: [], y: []})

    console.log("axis chart",axises)
    const options = {
        chart: {
            id: "basic-bar"
        },
        xaxis: {
            categories: axises.x
        }
    };
    const series = [
        {
            name: y_name,
            data: axises.y
        }
    ]


    return (
        // @ts-ignore
        <Chart
            options={options}
            series={series}
            type="bar"
            width="100%"
        />
    );

}
