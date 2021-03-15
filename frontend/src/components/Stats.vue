<template>
    <div  class="modal-wrapper" @mousedown="$emit('close')">
        <div class="modal-content" @mousedown.stop="">
            <h1>Example heading <span class="badge bg-secondary">New</span></h1>
            <button type="button" class="btn-close" aria-label="Close"></button>
            <button type="button" class="btn-close" aria-label="Close" @click="$emit('close')"></button>
            <!-- <table>
                <tr>
                    <td>Total Tweets</td>
                    <td>{{stats.total}}</td>
                </tr>
                <tr>
                    <td>Tweets in past day</td>
                    <td>{{stats.day}}</td>
                </tr>
                <tr>
                    <td>Tweets in past hour</td>
                    <td>{{stats.hour}}</td>
                </tr>
                <tr>
                    <td>Tweets in past minute</td>
                    <td>{{stats.minute}}</td>
                </tr>
            </table> -->
            <line-chart-container class="chart"/>
        </div>
    </div>
  
</template>

<script>
import LineChartContainer from "./LineChartContainer.vue"
export default {
    name: "Stats",
    components: {
        LineChartContainer,
    },
    data() {
        return {
            stats: null,
            r: null,
            isHidden: false,
        }
    },

    created() {this.get_stats()},

    methods: {
        get_stats() {
            fetch("http://localhost/api/stats/")
            .then(response => response.json())
            .then(json => {
                this.stats = json
            })
        }
    }
}
</script>

<style>


    .modal-content {
        padding: 10px;
        background: #ffffff;
        margin: auto;
        position: relative;
        width: 70%;
        height: 70%;
        border-radius: 4px;
        border: 2px solid rgba(0,0,0,0.2);
        background-clip: padding-box;
    }

    .modal-content span {
        line-height: 1;
        padding: 0 0 0 0;
        font-size: 18px;
    }

    .modal-wrapper {
        display: flex;
        text-align: center;
        z-index: 9998;
        top:0;
        left: 0;
        position:fixed;
        width: 100%;
        height: 100%;
        opacity: 1;
        background-color: rgba(29, 51, 59, 0.445);

    }

    .chart {
        padding: 1%;
        width: 100%;
        height: 10%;
    }
</style>