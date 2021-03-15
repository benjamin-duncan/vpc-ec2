<template>
    <div>
        <Tweet :id="tweetId" v-if="popped">
            <div class="load">    
                <div class="spinner-border" role="status">
                    <span class="sr-only">
                    </span>
                </div>
            </div>
        </Tweet>
    </div>
</template>

<script>
import {Tweet} from 'vue-tweet-embed'
import {LPopup} from 'vue2-leaflet'
export default {
    extends: LPopup,
    components: {Tweet},
    props: {
        tweetId:String(),
        popped: {
            type: Boolean,
            default: false,
        }

        },

}
</script>

<style>

    .load {
        height: 166px;
        align-content: center;
    }
</style>