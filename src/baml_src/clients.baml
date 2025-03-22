// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> Gemma3 {
  provider ollama
  options {
    base_url "http://localhost:11434/v1"
    model "gemma3:12b"
  }
}

// client<llm> Gemma3_12B {
//   provider ollama
//   options {
//     base_url "http://localhost:11434/v1"
//     model "gemma3:12b"
//   }
// }

// https://docs.boundaryml.com/docs/snippets/clients/retry
retry_policy Constant {
  max_retries 3
  // Strategy is optional
  strategy {
    type constant_delay
    delay_ms 200
  }
}

retry_policy Exponential {
  max_retries 2
  // Strategy is optional
  strategy {
    type exponential_backoff
    delay_ms 300
    mutliplier 1.5
    max_delay_ms 10000
  }
}