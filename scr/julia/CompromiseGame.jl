include("./Players.jl")

using Main.Players


mutable struct CompromiseGame
    p1::AbstractPlayer
    p2::AbstractPlayer
    npips::Int64
    length::Int64
    type::Char
    noties::Bool
    turn::Int64
    move1::Tuple{Int64,Int64,Int64}
    move2::Tuple{Int64,Int64,Int64}
    score1::Int64
    score2::Int64
    place1::Array{Tuple{Int64,Int64,Int64},1}
    place2::Array{Tuple{Int64,Int64,Int64},1}
    pips1::Array{Array{Array{Int64,1},1},1}
    pips2::Array{Array{Array{Int64,1},1},1}
    disp1::Array{Array{Array{Int64,1},1},1}
    disp2::Array{Array{Array{Int64,1},1},1}
end

function CompromiseGame(p1::AbstractPlayer, p2::AbstractPlayer, npips::Int, length::Int, type::Char, noties::Bool)
    return CompromiseGame(p1, p2, npips, length, type, noties,
        0, (0,0,0), (0,0,0), 0, 0,
        [(0,0,0) for i in 1:npips], [(0,0,0) for i in 1:npips],
        [ [ [ 0 for i in 1:3] for j in 1:3] for k in 1:3],
        [ [ [ 0 for i in 1:3] for j in 1:3] for k in 1:3],
        [ [ [ 0 for i in 1:3] for j in 1:3] for k in 1:3],
        [ [ [ 0 for i in 1:3] for j in 1:3] for k in 1:3] )
end

function CompromiseGame(p1::AbstractPlayer, p2::AbstractPlayer, npips::Int, length::Int, type::Char)
    return CompromiseGame(p1, p2, npips, length, type, true )
end

function CompromiseGame(p1::AbstractPlayer, p2::AbstractPlayer, npips::Int, length::Int)
    return CompromiseGame(p1, p2, npips, length, 's' )
end

function reset!(g::CompromiseGame)
    g.turn = 0
    g.score1 = 0
    g.score2 = 0
    g.move1 = (0,0,0)
    g.move2 = (0,0,0)
    g.pips1 = [ [ [ 0 for i in 1:3] for j in 1:3] for k in 1:3]
    g.pips2 = [ [ [ 0 for i in 1:3] for j in 1:3] for k in 1:3]
    g.disp1 = [ [ [ 0 for i in 1:3] for j in 1:3] for k in 1:3]
    g.disp2 = [ [ [ 0 for i in 1:3] for j in 1:3] for k in 1:3]
    return
end

function new_players!(g::CompromiseGame, p1::AbstractPlayer, p2::AbstractPlayer)
    g.p1 = p1
    g.p2 = p2
    reset!(g)
    return
end

function prepare_disposable!(g::CompromiseGame)
    for i in 1:3
        for j in 1:3
            for k in 1:3
                g.disp1[i][j][k] = g.pips1[i][j][k]
                g.disp2[i][j][k] = g.pips2[i][j][k]
            end
        end
    end
    return
end

function round!(g::CompromiseGame)
    g.turn += 1
    if g.type == 's'
        for i in 1:g.npips
            g.pips1[rand(1:3)][rand(1:3)][rand(1:3)] += 1
            g.pips2[rand(1:3)][rand(1:3)][rand(1:3)] += 1
        end
    else
        prepare_disposable!(g)
        place_pips!(g.p1, g.place1, g.disp1, g.disp2, g.score1, g.score2, g.move1, g.move2, g.turn, g.length, g.npips)
        prepare_disposable!(g)
        place_pips!(g.p2, g.place2, g.disp2, g.disp1, g.score2, g.score1, g.move2, g.move1, g.turn, g.length, g.npips)
        for i in 1:g.npips
            g.pips1[g.place1[i][1]][g.place1[i][2]][g.place1[i][3]] += 1
            g.pips2[g.place2[i][1]][g.place2[i][2]][g.place2[i][3]] += 1
        end
    end

    if g.type == 'g'
        g.move1 = (rand(1:3), rand(1:3), rand(1:3))
        g.move2 = (rand(1:3), rand(1:3), rand(1:3))
    else
        prepare_disposable!(g)
        g.move1 = make_move!(g.p1, g.disp1, g.disp2, g.score1, g.score2, g.place1, g.place2, g.turn, g.length, g.npips)
        prepare_disposable!(g)
        g.move2 = make_move!(g.p2, g.disp2, g.disp1, g.score2, g.score1, g.place2, g.place1, g.turn, g.length, g.npips)
    end

    for i in 1:3
        for j in 1:3
            for k in 1:3
                if !(i==g.move1[1] || i==g.move2[1] || j==g.move1[2] || j==g.move2[2] || k==g.move1[3] || k==g.move2[3] )
                    g.score1 += g.pips1[i][j][k]
                    g.score2 += g.pips2[i][j][k]
                    g.pips1[i][j][k] = 0
                    g.pips2[i][j][k] = 0
                end
            end
        end
    end
end

function play!(g::CompromiseGame)
    reset!(g)
    while g.turn < g.length || (g.noties && g.score1 == g.score2)
        round!(g)
    end
    return (g.score1, g.score2)
end

p = RandomPlayer()

g = CompromiseGame(p,p,200,1,'c')

play!(g)
