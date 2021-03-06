<template>
    <div>
        <p>{{healthCheck}}<p/>
    </div>
</template>

<script>
export default {
    name: "get-request",
    data() {
        return {
            healthCheck: null
        };
    },
    created() {
        fetch("http://localhost/health/",{
        headers:{"Access-Control-Allow-Origin": "*"}
        })
            .then(response => {if(response.status==200){
                this.healthCheck="Status Code: 200 OK"
                }})
            // .then(data => (this.healthCheck = data+"Health Check Succeeded!"))
    }

}
</script>

<style>

</style>