const goods = [
    {title: 'Shirt', price: 150},
    {title: 'Socks', price: 50},
    {title: 'Jacket', price: 350},
    {title: 'Shoes', price: 250},
];

class GoodsItem {
    constructor({title, price}) {
        this.title = title;
        this.price = price;
    }
    render() {
        return `<div class="goods-item">
                    <h3>${this.title}</h3>
                    <p>${this.price}</p>
                </div>`
    }
}

class GoodsList {
    constructor(dataList) {
        this.dataList = dataList;
    }
    getSum() {
        return this.dataList.reduce((prev, {price}) => prev + price, 0)
    }
    render () {
        const dataItems = this.dataList.map(
            item => {
                const dataItem = new GoodsItem(item);
                return dataItem.render();
            }
        )
        document.querySelector('.goods-list').innerHTML = dataItems.join('');
    }
    filterGoods(value) {
        pass
    }
}

searchButton.addEventListener('click', e => {
    const value = searchInput.value;
    list
})

class Basket {
    setVision() {}
    render() {}
}

class BasketItem {
    setCount() {}
    deleteItem() {}
    render() {}
}

onload = () => {
    const goodsList = new GoodsList(goods);
    goodsList.render();
}

// const renderGoodsItem = ({title, price}) => 
// `<div class="goods-item">
//     <h3>${title}</h3>
//     <p>${price}</p>
// </div>`;

// const renderGoodsList = list => {
//     let goodList = list.map(item => renderGoodsItem(item));
//     document.querySelector('.goods-list').innerHTML = goodList.join('');
// };

// renderGoodsList(goods);