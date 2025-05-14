const product = [
    {
        id:0,
        image: src="img/dopamine.png",
        title: "Dopamine",
        price: 50
    },
    {
        id:1,
        image: "img/mythOfNormal.png",
        title: "The Myth Of Normal",
        price: 70
    },
    // {
    //     id:2,
    //     image: './self-help/whenTheBodySayNo.png',
    //     title: "When The Body Says No",
    //     price: 70
    // },
    {
        id:3,
        image: "img/mythOfNormal.png",
        title: "The Body Keeps The Score",
        price: 100
    },
    {
        id:4,
        image: "img/letThem.png",
        title: "Let Them",
        price: 60
    }
] 

const books = [...new Set(product.map((item)=>{return item}))]

let i = 0;
document.getElementById("root").innerHTML = books.map((item)=>{
   
    let {image, title, price} = item;
    
    return `<div class="box">
        <div class="img-box">
            <img class= "images" src="${image}"></img>
            </div>
        <div class= "bottom">
        <p class="title">${title}</p>
        <h2>$ ${price}.00</h2>
    `+ "<button onclick='addtocart("+(i++)+")'>Add to cart</button>"+
    `</div>
    </div>`
}).join("")

let cart = [];

function addtocart(a){
    cart.push({...books[a]});
    displaycart();
}

function delElement(a){
    cart.splice(a,1);
    displaycart()
}

function displaycart(a){
    let j = 0; total = 0;
    document.getElementById("count").innerHTML = cart.length;
    if(cart.length == 0){
        document.getElementById('cartItem').innerHTML = "Your cart is empty";
        document.getElementById('total').innerHTML = "$ "+0+".00"
    }else{
        document.getElementById('cartItem').innerHTML = cart.map((items)=>{
            let {image, title, price} = items;
            total = total+price;
            document.getElementById("total").innerHTML = "$ "+total+".00";
            return (
                `<div class='cart-item'>
                <div class= 'row-img'>
                    <img class= 'rowimg' src=${image}>
                </div>
                <p style = 'font-size:12px;'>${title}</p>
                <h2 style = 'font-size:12px;'>$ ${price}.00</h2>`+
                "<i class= 'fa-solid fa-trash' onclick='delElement("+ (j++) +")'></i></div>"
            );
        }).join("")
    }
}