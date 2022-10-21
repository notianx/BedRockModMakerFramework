
from main.block.BlockHandler import BlockHandler
from main.entity.MobHandler import MobHandler
from main.item.ItemHandler import ItemHandler
from main.Sql import SqlCls

if (__name__ == '__main__'):

    print("请选择：\n"
          "0.配置所有\n"
          "1.配置生物\n"
          "2.配置物品\n"
          "3.配置方块\n"
          "4.清理")

    choice = int(input())

    if choice == 0:
        ItemHandler().deal()
        print("\nItem Successful\n")
        BlockHandler().deal()
        print("\nBlock Successful\n")
        MobHandler().deal()
        print("\nEntity Successful\n")
    elif choice == 1:
        MobHandler().deal()
        print("\nEntity Successful\n")
    elif choice == 2:
        ItemHandler().deal()
        print("\nItem Successful\n")
    elif choice == 3:
        BlockHandler().deal()
        print("\nBlock Successful\n")
    elif choice == 4:
        ItemHandler.clear()
        BlockHandler().clear()
        MobHandler.clear()
        print("\nClear Successful\n")
    else:
        print("You is a pig")

    SqlCls.mainDo()
