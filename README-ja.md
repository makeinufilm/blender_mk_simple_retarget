<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/181dde7c-1697-43a9-a993-6041fa96409b" width="256"><br>
blenderを日本語で使用してる人は新規データのチェックを外して利用する事をお勧めします（今後のik対応で安定しない可能性があります）
# 1.first:
概要：<br>
※このアドオンは公開したばかりで、あらゆる状況のリグに対応出来ている訳ではありません、なるべく対応はします<br>
但し、骨の向きや構成によって正しいリターゲットが出来るかは保証できません
　もし対応を依頼したい場合又はエラー報告はoshigoto@makeinufilm.comまでご連絡下さい（対応に時間が掛かる場合があります、法人様の場合はプロジェクトの規模によっては有償対応の可能性があります）
 　
<br><br>  環境と操作手順やリグの構成によってはエラーが出ます、諸々の動作を保証できないので<br>
予めご了承下さい（操作手順とエラー文を送ってもらえれば出来る限り対応します）
<br>※※ボーンレイヤ、ボーンコレクションのAPIがblender3.6とblender4.0で異なる為4.0以降の対応はblender4.3LTSがリリースされてから始める予定です
動作検証はblender3.6.2で行っています<br>
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/1a9aeebd-f8ad-4b23-a2b8-584625388d8b" width="768">

※画像はオリジナルキャラの千代とMoMaskでtext to motionを行ったbvhデータです
# 2.UI description:
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/18bd42b6-112e-4824-b4c9-d132726f3606" width="768">
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/faefc9f3-efe2-49a2-8313-2749b594a71c" width="768">

# 3.process description:

設定例：<br>
#### １．諸々アーマチュアとボーンの名前の登録
<br>　終わったらUIが画像みたいな感じになると思います
<br>　*arms_groupとlegs_groupが一部空白になっていますがmomaskBVHだと手首がZUP方向に向いているので<br>空白にしています（手首部分が空白の場合はX軸に向くように設定しています）
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/d155d704-df2c-4f41-8166-ae14438b0cb3" width="768"><br>
#### ２．retarget_setting(FK_only)
　　押すとコンストレイントが割り当てられ同時にコンストレイントの影響値がRetargetOffsetPanelに表示されます<br><br>
　　**Z方向に飛んでしまった場合はOffsetのチェックボックスを外してください**<br>
　　root_offsetZは縦方向の補正、root_offsetXYは横方向の補正です、適宜調整してください<br>
<br>
　　他、骨の名前とInfluenceが表示されます、回転を反映したくない所を適宜調整（例：首と頭のブレを抑える為にNeckとHeadをオフ）<br>
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/3bd9cda6-02be-4161-9a57-ccc2e2e21a11" width="768">
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/790326c8-951d-4c60-861a-7b5415881612" width="768"><br>
#### ２－clear_setting
押すと元の設定に戻ります
　※"MK_"という接頭辞が付いた骨、コンストレイントを削除するので、もし同名の骨がある場合は予めリネームをしてください
 
#### ３．Bake_Animation

<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/e9b169d3-b6ab-4614-a87d-e1721102f00a" width="768"><br>
登録しているターゲットボーンのみにアニメーションの焼き付けを行います、完了です
#### ４．IK_offset(Features not completed)
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/27eff023-ad47-43ea-8b6c-91581a59c4d3" width="768"><br>
4.3LTSが来たら多分……やります……。
色々整理されてませんがとりあえずRootの位置と足と手の位置調整(_OFST_)が行える機能……ですが、現時点では不安定です
<br>Bake_AnimationをするとIKではなく登録したFK（デフォーム）ボーンのみBakeが行われて、IKに関わる骨は削除されます

## Operations that lead to errors:
操作によってはエラーが出ます<br>
１．ソースボーンとターゲットボーンはハイド（非表示）[ショートカット：H]をしないでください<br>
２．コントロールリグがある場合はuse IK offsetにチェックを入れないでください<br>
３．コントロールリグが無い場合で捻りジョイントtwistジョイントの仕組みがある場合等もIK offsetは非推奨です（今後対応します）<br>
４．FBXをそのままインポートするとスケール0.01になる事が多いです、やむを得ず0.01のままでリターゲットを行う場合は：Apply：(適用)のデルタスケールを適用を行ってください<br>
　　※但しこの場合でも座標位置が飛ぶ事があるので、**出来れば等倍設定で**使用してください<br>
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/8ae4db7b-8d6b-4cc9-92c5-a8adab491f59" width="384"><br>
<br>※↑は他DCCで書き出されたFBXをインポートする際の参考、スケールは100、Automatic Bone Orientationにチェック<br>
　インポート完了後手動で読み込まれたFBXのオブジェクトを全選択してスケールを一致させて：Apply：(適用) All Transoform で正規化してください<br>


## AIによるおまけのblender登録方法

こんにちは、Blenderのユーザーの皆様。私たちは、あなたがBlenderでのアニメーション作業をより簡単に、より効率的に行えるように開発された新しいアドオンをご紹介します。その名も「MK Simple Retarget」です。

このアドオンは、アニメーションリターゲットを主な機能としています。つまり、一つのアニメーションを別のキャラクターに適用することが可能になります。これにより、一度作成したアニメーションを再利用して、さまざまなキャラクターに適用することができます。

このアドオンをBlenderに登録する方法は以下の通りです：

Blenderを開き、上部メニューの「Edit」をクリックします。
「Preferences」を選択します。
開いたウィンドウの左側にあるメニューから「Add-ons」をクリックします。
右上にある「Install…」ボタンをクリックします。
ダウンロードした「mk_simple_retarget_00.py」を選択し、「Install Add-on」ボタンをクリックします。
インストールしたアドオンがリストに表示されるので、チェックボックスをオンにして有効化します。<br>
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/80f670bf-90dc-4b33-a8b6-78212449e970" width="768"><br>

以上で、「MK Simple Retarget」のインストールと有効化が完了しました。これで、あなたもアニメーションリターゲットの力を存分に利用することができます。ぜひ、このアドオンを使って、あなたのアニメーション作成をより楽しく、より効率的にしてみてください。

それでは、ハッピーブレンディング！

上記の挨拶はbingAIが書いています、ハッピーブレンディングとはなんなんでしょう


This add-on has just been released and is not compatible with all rigs in all situations. We will do our best, but we cannot guarantee that it will retarget correctly depending on the orientation and configuration of the bones.
　If you would like to request a response (although it may take some time), please contact us at oshigoto@makeinufilm.com (for corporate clients, depending on the size of the project, there may be a possibility of a paid response).
 　Please note that errors may occur depending on the environment, operating procedures, and rig configuration, and we cannot guarantee the operation of the rig (if you send us the operating procedures and error messages, we will do our best to respond).
**Because the bone layer and bone collection APIs are different between blender 3.6 and blender 4.0, we plan to start supporting blender 4.0 and later after blender 4.3 LTS is released.
The operation has been verified with blender 3.6.2.
Hello, Blender users! We are excited to introduce a new add-on developed to make your animation work in Blender easier and more efficient. It’s called “MK Simple Retarget”.

The main feature of this add-on is animation retargeting. This means you can apply one animation to another character. This allows you to reuse an animation you’ve created and apply it to various characters.

Here’s how to register this add-on in Blender:

Open Blender and click on “Edit” in the top menu.
Select “Preferences”.
From the menu on the left side of the window that opens, click on “Add-ons”.
Click on the “Install…” button at the top right.
Select the downloaded “mk_simple_retarget_00.py” and click the “Install Add-on” button.
The installed add-on will appear in the list. Enable it by checking the checkbox.
With that, you’ve successfully installed and enabled “MK Simple Retarget”. Now you can fully utilize the power of animation retargeting. Try using this add-on to make your animation creation more enjoyable and efficient.

For more details, please check the GitHub link below: GitHub Link

Happy Blending!

*The above greeting is written by bingAI What is happyblending, please tell me.

# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details
