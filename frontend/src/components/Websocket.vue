<template>
<div>
    <p>{{message}}</p>
  <!-- <button @click="disconnect" v-if="status === 'connected'">Disconnect</button>
  <button @click="connect" v-if="status === 'disconnected'">Connect</button> {{ status }} -->
  <br /><br />
  <div v-if="status === 'connected'">
    <!-- <form @submit.prevent="sendMessage" action="#">
      <input v-model="message"><button type="submit">Send Message</button>
    </form> -->
    <!-- <ul id="logs">
      <li v-for="log in logs" :key="log.id" class="log">
        {{ log.event }}: {{ log.data }}
      </li>
    </ul> -->
  </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            message: "",
            logs: [],
            status: "disconnected"
        }
    },

    created() {
        this.connect()
    },

    methods: {
        connect() {
            this.socket = new WebSocket("ws://localhost/ws/tweets/");
            this.socket.onopen = () => {
                this.status = "connected";
                // this.logs.push({ event: "Connected to", data: 'ws://localhost/ws/tweets/'});
                

                this.socket.onmessage = ({data}) => {
                    // this.logs.push({ event: "Recieved message", data });
                    this.message=JSON.parse(JSON.parse(data).message)[0].fields.text
                };
            };
        },
        disconnect() {
            this.socket.close();
            this.status = "disconnected";
            this.logs = [];
        },
        
    }
}
// eslint-disable-next-line no-use-before-define
    //     sendMessage(e) {
    //     this.socket.send(this.message);
    //     this.logs.push({ event: "Sent message", data: this.message });
    //     this.message = "";
    //     }
    // }}
</script>

<style>
</style>
