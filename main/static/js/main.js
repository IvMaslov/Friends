function logout() {
    window.location.href = "logout"
  }

  function addFriendOpen() {
    document.getElementById("backWithOpacity").style.display = "block"
    document.getElementById("addFrWin").style.display = "flex"

  }

  function addFriendClose() {
    document.getElementById("usernameIpt").value = ""
    document.getElementById("errorLabel").style.display = "none"
    document.getElementById("backWithOpacity").style.display = "none"
    document.getElementById("addFrWin").style.display = "none"
  }

  async function sendRequestForFriendship() {
    response = await fetch("request_for_friendship" + "?" + new URLSearchParams({
      username: document.getElementById("usernameIpt").value
    }),{
      method: "GET",
    })
    if (response.status === 200) {
      addFriendClose()
      fillFriends()
      fillIncoming()
      fillOutgoing()
    } else {
      document.getElementById("errorLabel").style.display = "block"
    }
  }

  function checkStatusOpen() {
    document.getElementById("backWithOpacity").style.display = "flex"
    document.getElementById("checkStatWin").style.display = "flex"
  }

  function checkStatusClose() {
    document.getElementById("usernameIptCS").value = ""
    document.getElementById("errorLabelCS").style.display = "none"
    document.getElementById("backWithOpacity").style.display = "none"
    document.getElementById("status").style.display = "none"
    document.getElementById("checkStatWin").style.display = "none"
  }

  async function sendRequestCheckStatus() {
    response = await fetch("check_status" + "?" + new URLSearchParams({
      username: document.getElementById("usernameIptCS").value
    }),{
      method: "GET",
    })
    if (response.status === 200) {
      data = await response.json()
      document.getElementById("errorLabelCS").style.display = "none"
      document.getElementById("status").style.display = "block"
      switch (data.status) {
        case 0:
          document.getElementById("status").textContent = "Not Friends"
          break;
        case 1:
          document.getElementById("status").textContent = "Incoming Request"
          break;
        case 2:
          document.getElementById("status").textContent = "Outcoming Request"
          break;
        case 3:
          document.getElementById("status").textContent = "Friends"
          break;
        default:
          document.getElementById("errorLabelCS").style.display = "block"
          document.getElementById("status").style.display = "none"
          break;
      }
    } else {
      document.getElementById("errorLabelCS").style.display = "block"
      document.getElementById("status").style.display = "none"
    }
  }

  function deleteFriendOpen() {
    document.getElementById("backWithOpacity").style.display = "flex"
    document.getElementById("delFrWin").style.display = "flex"
  }

  function deleteFriendClose() {
    document.getElementById("usernameIptDlt").value = ""
    document.getElementById("errorLabelDlt").style.display = "none"
    document.getElementById("backWithOpacity").style.display = "none"
    document.getElementById("delFrWin").style.display = "none"
  }

  async function sendDeleteFriend() {
    response = await fetch("delete_friend" + "?" + new URLSearchParams({
      username: document.getElementById("usernameIptDlt").value
    }),{
      method: "GET",
    })
    if (response.status === 200) {
      deleteFriendClose()
      fillFriends()
      fillIncoming()
      fillOutgoing()
    } else {
      document.getElementById("errorLabelDlt").style.display = "block"
    }
  }

  async function fillFriends() {
    response = await fetch("friends", {
      method: "GET"
    })
    if (response.status === 200) {
      let data = await response.json()

      let parent = document.getElementById("friends")
      parent.innerHTML = ""
      for (let i = 0; i < data.friends.length; i++) {
        let elem = document.createElement("span")
        elem.classList.add("table-elem")
        elem.textContent = data.friends[i].username
        parent.appendChild(elem)
      }
      if (data.friends.length === 0) {
        let elem = document.createElement("span")
        elem.classList.add("emptyElem")
        elem.textContent = "No Friends"
        parent.appendChild(elem)
      }
    }
  }

  async function fillIncoming() {
    response = await fetch("incoming", {
      method: "GET"
    })
    if (response.status === 200) {
      let data = await response.json()

      let parent = document.getElementById("incoming")
      parent.innerHTML = ""
      for (let i = 0; i < data.incoming.length; i++) {
        let elem = document.createElement("div")
        elem.classList.add("wrapperForIncomingElem")
        let span = document.createElement("span")
        let okbtn = document.createElement("button")
        okbtn.classList.add("okBtn")
        okbtn.textContent = "OK"
        let notbtn = document.createElement("button")
        notbtn.classList.add("notBtn")
        notbtn.textContent = "X"
        elem.appendChild(span)
        elem.appendChild(okbtn)
        elem.appendChild(notbtn)

        elem.classList.add("table-elem")
        elem.classList.add("incoming-elem")
        elem.tabIndex = i
        elem.addEventListener("focus", onFocus)
        elem.addEventListener("blur", onBlur)
        span.textContent = data.incoming[i].username

        parent.appendChild(elem)
      }
      if (data.incoming.length === 0) {
        let elem = document.createElement("span")
        elem.classList.add("emptyElem")
        elem.textContent = "No Incoming"
        parent.appendChild(elem)
      }
    }
  }

  async function fillOutgoing() {
    response = await fetch("outgoing", {
      method: "GET"
    })
    if (response.status === 200) {
      let data = await response.json()

      let parent = document.getElementById("outgoing")
      parent.innerHTML = ""
      for (let i = 0; i < data.outgoing.length; i++) {
        let elem = document.createElement("span")
        elem.classList.add("table-elem")
        elem.textContent = data.outgoing[i].username
        parent.appendChild(elem)
      }
      if (data.outgoing.length === 0) {
        let elem = document.createElement("span")
        elem.classList.add("emptyElem")
        elem.textContent = "No Outgoing"
        parent.appendChild(elem)
      }
    }
  }

  function onFocus() {
    this.children[1].style.display = "block"
    this.children[2].style.display = "block"
    this.children[1].onmousedown = acceptReq
    this.children[2].onmousedown = refuseReq
  }

  function onBlur() {
    this.children[1].style.display = "none"
    this.children[2].style.display = "none"
    this.children[1].onmousedown = null
    this.children[2].onmousedown = null
  }

  async function acceptReq() {
    let response = await fetch("accept" + "?" + new URLSearchParams({
      username: this.parentNode.children[0].textContent
    }), {
      method: "GET"
    })
    if (response.status === 200) {
      fillFriends()
      fillIncoming()
      fillOutgoing()
    }
  }

  async function refuseReq() {
    let response = await fetch("refuse" + "?" + new URLSearchParams({
      username: this.parentNode.children[0].textContent
    }), {
      method: "GET"
    })
    if (response.status === 200) {
      fillFriends()
      fillIncoming()
      fillOutgoing()
    }
  }

  async function start() {
      response = await fetch("user", {
          method: "GET"
      })
      if (response.status === 200) {
          data = await response.json()
          document.getElementById("username").textContent = data.username
      }
  }
  start()
  fillFriends()
  fillIncoming()
  fillOutgoing()