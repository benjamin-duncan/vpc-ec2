<template>

  <div class='custom-popup' id="map-wrapper">
    <l-map
      :zoom="zoom"
      :center="center"
      style="height: 100%, width: 100%"
      :options="mapOptions"
      ref="myMap"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
        :options="tileOptions"
      />

      <tweet-marker
        v-for="marker in markers"
        :key="marker.id"
        :visible="markers.visible"
        :icon="marker.icon"
        :lat-lng.sync="marker.position"
        :id="marker.tweetId"
        @click="marker.popped=true"
        class="marker"
      >
        <transition name="fade">
        <tweet-popup
          :options="popupOptions"
          :tweetId="marker.tweetId"
          :popped="marker.popped"
        >
        </tweet-popup>      
        </transition>
      </tweet-marker>

    </l-map>
    <stats v-if="showModal" @close="showModal=false"></stats>

    <svg xmlns="http://www.w3.org/2000/svg" width="37" height="37" fill="currentColor" class="info-circle" viewBox="0 0 16 16" @click="showModal=true">
    <p>Stats</p>
    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
    <path d="M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
    </svg>
    </div>
</template>
<script>
import { latLng, } from "leaflet";
import { LMap, LTileLayer} from "vue2-leaflet";
import Stats from "./Stats.vue";
import TweetMarker from "./TweetMarker.vue"
import TweetPopup from "./TweetPopup.vue"
// import PopupTweet from './PopupTweet.vue'
// import {Tweet} from "vue-tweet-embed"

export default {
  name: "Example",
  components: {
    LMap,
    LTileLayer,
    TweetMarker,
    TweetPopup,
    Stats,
  },
  data() {
    return {

      // websocket
      message: "",
      logs: [],
      status: "disconnected",

      // map
      zoom: 6,
      center: latLng(55, -3),
      url: 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      mapOptions: {
        zoomSnap: 1,
      },
      tileOptions: {
        tileSize: 512,
        zoomOffset: -1,
      },
      popupOptions: {
        minWidth: 250,
        maxWidth: 1000,
        minHeight: 350,
      },

      markers: [],
      tweet: "",
      show: false,
      showit: 0,

      showModal: false,
    };
  },

  created() {
      this.connect()

      // this.$nextTick(() => {
      //   // this.$refs.myMap.mapObject.openPopup(<p>hello</p>,[0,0])
      //   console.log(this.$refs.myMap.mapObject.getCenter())
      //   var marker = L.marker([55, -3])
      //   marker.addTo(this.$refs.myMap.mapObject).on('click',this.logit("test"));
      //   // this.markers.push(marker)
      // })
    },

  methods: {
    connect() {
      this.socket = new WebSocket("ws://localhost/ws/tweets/");
      this.socket.onopen = () => {
        this.status = "connected";
          

          this.socket.onmessage = ({data}) => {
              this.message=JSON.parse(JSON.parse(data).message)[0].fields
              console.log(this.message)
              const timestampMarker= {
                timestamp: this.message.timestamp_ms,
                timestampAdded: Date.now(),
                tweetId: String(this.message.tweet_id),
                position: {lat: this.message.lon, lng: this.message.lat},
                visible: "true",
                popped: false
              }
              this.markers.push(timestampMarker)
              if(this.markers.length >=100){
                this.disconnect()
              }              
              // if(this.markers.length >=100){
              //   this.markers.splice(0,1)
              // }
          };
      };
    },
    disconnect() {
        this.socket.close();
        this.status = "disconnected";
        this.logs = [];
    },
    
    showTweet(id) {
      this.tweet=id
    },
    showittt(){
      this.showit=!this.showit
    },
    logit(test){
      console.log(test)
    }


  }
};
</script>

<style >

  #map-wrapper {
    height: 100%;
    margin: 0;
  }

  /* /deep/ LPopup {
    background: black;
  } */
    /* .custom-popup .leaflet-popup-content-wrapper a {
    color:rgba(255,255,255,0.5);
    } */
  /* .custom-popup .leaflet-popup-tip-container {
    width:30px;
    height:15px;
    } */
  
  .custom-popup .leaflet-popup-content-wrapper {
    font-size:16px;
    line-height:24px;
    background: white;
    border-radius: 20px;
    padding: 0px 0px;
    border-color: transparent;
    box-shadow: 0;
    }
  .custom-popup .leaflet-popup {
    margin-bottom: 10px;
  }

  .custom-popup .leaflet-popup-tip {
    background: white;
    height: 17px;
    margin: -10px auto 0;
    border-radius: 0px;
    }

  .custom-popup .leaflet-popup-tip-container {
    height:20px;
    /* margin: 0; */
    overflow: hidden;
    margin: -10px -20px;
  }
  .custom-popup .leaflet-popup-content{
    margin: 0;
    color: black;
    line-height: 1;
    text-align: center;
    vertical-align: middle;
  }

  .custom-popup .leaflet-container a.leaflet-popup-close-button {
	top: 2px;
  right: -8px;
  padding: 0px 0px 0px 0px;
  color: #747474;
  border: 1px solid rgb(189, 189, 189);
  background: rgb(255, 255, 255);
  height: 18px;
  border-radius: 10px;
  vertical-align:50%;
  line-height: 1;
  } 
  

  .info-circle {
    z-index: 1000;
    top:22px;
    left: 60px;
    position: absolute;
    color:black;
    background-color:#ffffff;
    background-clip: padding-box;
    padding: 5px 5px;
    /* box-shadow: 0 0 5px grey; */
    border: 2px solid rgba(0,0,0,0.2);
    border-radius: 4px;
    cursor:pointer;
  }

  .marker {
    image-orientation: 90deg;
  }

  .fade-enter-active, .fade-leave-active {
  transition: opacity 3s;
  }

  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }
</style>