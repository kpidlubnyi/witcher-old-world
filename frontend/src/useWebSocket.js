import { ref } from "vue"


export function useWebSocket(url) {
    const data = ref(null)
    const connected = ref(false)
    let ws
    
    const connect = () => {
        ws = new WebSocket(url)

        ws.onopen = () => connected.value = true
        ws.onclose = () => connected.value = false

        ws.onmessage = (e) => {
            data.value = JSON.parse(e.data)
        }
    }

    const send = (msg) => {
        ws?.send(JSON.stringify(msg))
    }

    return { data, connected, connect, send }
}
